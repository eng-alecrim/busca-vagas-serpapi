# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================


import hashlib
import logging
import logging.config
import pickle
import shutil
from functools import reduce
from pathlib import Path
from typing import Union

import pandas as pd

from busca_vagas_serpapi.busca_vagas import loop_busca
from busca_vagas_serpapi.schemas import FilaBuscas
from busca_vagas_serpapi.utils_vagas import df_resultados

# =============================================================================
# CONSTANTES
# =============================================================================

logging.config.fileConfig("config/logging.toml")
LOGGER = logging.getLogger("logMain.info.debug")

MAX_ERROS_CONSULTA = 5

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Função para salvar a fila de buscas em um arquivo pickle
# -----------------------------------------------------------------------------


def salva_fila(fila_buscas: FilaBuscas, dir: Path) -> None:
    with open(dir / "fila.pkl", "wb") as pkl_f:
        pickle.dump(obj=fila_buscas, file=pkl_f)


# -----------------------------------------------------------------------------
# Função para carregar a fila de buscas de um arquivo pickle
# -----------------------------------------------------------------------------


def load_fila(path_fila_buscas: Union[str, Path]) -> FilaBuscas:
    with open(path_fila_buscas, "rb") as pkl_f:
        fila = pickle.load(file=pkl_f)
    return fila


# -----------------------------------------------------------------------------
# Função para empilhar arquivos de busca em um único arquivo Parquet
# -----------------------------------------------------------------------------


def empilha_fila(path_buscas: Union[str, Path], nome_arquivo: str) -> None:
    path_buscas = path_buscas if isinstance(path_buscas, Path) else Path(path_buscas)
    arquivos = path_buscas.rglob("*.parquet")
    f_reduce = lambda dfs, path_: dfs + [pd.read_parquet(path_)]
    dfs = reduce(f_reduce, arquivos, [])
    df = pd.concat(dfs).fillna("N/A")
    df.to_parquet(path_buscas.parent / f"{nome_arquivo}.parquet", index=False)
    shutil.rmtree(path_buscas)
    LOGGER.debug(f"path_buscas: diretório temporário '{path_buscas}' removido.")

    return None


# -----------------------------------------------------------------------------
# Função para realizar a pesquisa de vagas baseada na fila de buscas
# -----------------------------------------------------------------------------


def pesquisa_fila(fila_buscas: FilaBuscas) -> None:
    dir_destino = (
        fila_buscas.diretorioDestino
        if isinstance(fila_buscas.diretorioDestino, Path)
        else Path(fila_buscas.diretorioDestino)
    )
    LOGGER.debug(f"pesquisa_fila: diretório destino -> '{dir_destino}'.")
    dir_temp = dir_destino / hashlib.md5(fila_buscas.nomeArquivo.encode()).hexdigest()
    dir_temp.mkdir(exist_ok=True, parents=True)
    LOGGER.info(f"pesquisa_fila: '{dir_temp}' criado.")

    i = 1
    n_erros = 0
    len_inicial = len(fila_buscas.buscas)

    while fila_buscas.buscas:
        if n_erros < MAX_ERROS_CONSULTA:
            busca = fila_buscas.get_busca()
            LOGGER.debug(f"pesquisa_fila: ({i}/{len_inicial})")
            try:
                resultados = loop_busca(busca)
                assert resultados is not None, "pesquisa_fila: resultados is None"

                vagas_busca = df_resultados(resultados)
                vagas_busca["BUSCA"] = busca.q
                LOGGER.debug("pesquisa_fila: DataFrame criado.")

                path_destino = dir_temp / f"{fila_buscas.nomeArquivo}_{i}.parquet"
                vagas_busca.to_parquet(path_destino, index=False)
                LOGGER.info(f"pesquisa_fila: busca exportada para '{path_destino}'.")

                LOGGER.info(f"pesquisa_fila: '{busca.q}' removido da fila.")

                i += 1
                n_erros = 0

            except Exception as e:
                LOGGER.warning(f"pesquisa_fila: AVISO! {e}")
                fila_buscas.add_busca(busca)
                n_erros += 1
        else:
            salva_fila(fila_buscas, dir_temp)
            LOGGER.warning(
                f"pesquisa_fila: ERRO! Fila foi salva em '{dir_temp}/fila.pkl'."
            )
            busca = fila_buscas.get_busca()
            raise RecursionError(
                f"pesquisa_fila: ERRO! A busca '{busca.q}' falhou mais de 5 vezes!"
            )

    empilha_fila(dir_temp, fila_buscas.nomeArquivo)
    LOGGER.info(
        f"pesquisa_fila: Vagas empilhadas e salvas em '{dir_destino / fila_buscas.nomeArquivo}.parquet'."
    )

    return None
