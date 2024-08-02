# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import os
from functools import reduce
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import find_dotenv, load_dotenv
from pandas import DataFrame

from .schemas import RegistroVaga
from .utils import get_path_projeto

# =============================================================================
# CONSTANTES
# =============================================================================

load_dotenv(find_dotenv())
API_SERPAPI = os.getenv("API_SERPAPI", "")
assert (
    API_SERPAPI is not None
), "utils_vagas: FORNEÇA A CHAVE DA API NO ARQUIVO .env!"

DIR_PROJETO = get_path_projeto()
assert isinstance(DIR_PROJETO, Path)
PATH_PARAMETROS_BUSCAS = DIR_PROJETO / "config/parametros_buscas.yaml"

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Função para obter as qualificações da vaga
# -----------------------------------------------------------------------------


def get_qualificacoes(job: Dict) -> Optional[str]:
    highlights = job.get("job_highlights")
    if highlights is None:
        return None

    for highlight in highlights:
        if highlight.get("title") == "Qualifications":
            items = highlight.get("items")
            qualificacoes = "; ".join(items) if items is not None else None
            return qualificacoes

    return None


# -----------------------------------------------------------------------------
# Função para obter as responsabilidades da vaga
# -----------------------------------------------------------------------------


def get_responsabilidades(job: Dict) -> Optional[str]:
    highlights = job.get("job_highlights")
    if highlights is None:
        return None

    for highlight in highlights:
        if highlight.get("title") == "Responsibilities":
            items = highlight.get("items")
            responsabilidades = "; ".join(items) if items is not None else None
            return responsabilidades

    return None


# -----------------------------------------------------------------------------
# Função para obter os benefícios da vaga
# -----------------------------------------------------------------------------


def get_beneficios(job: Dict) -> Optional[str]:
    highlights = job.get("job_highlights")
    if highlights is None:
        return None

    for highlight in highlights:
        if highlight.get("title") == "Benefits":
            items = highlight.get("items")
            beneficios = "; ".join(items) if items is not None else None
            return beneficios

    return None


# -----------------------------------------------------------------------------
# Função para gerar um registro de vaga
# -----------------------------------------------------------------------------

gera_registro = lambda job: RegistroVaga(
    ID_VAGA=job.get("job_id"),
    DATA_CONSULTA=job.get("created_at"),
    TITULO=job.get("title").strip(),
    EMPRESA=job.get("company_name").strip(),
    LOCAL=job.get("location", "N/A").strip(),
    ANUNCIANTE=job.get("via").strip(),
    DESCRICAO=job.get("description").strip(),
    POSTADO_EM=job.get("detected_extensions", {}).get("posted_at"),
    REGIME=job.get("detected_extensions", {}).get("schedule_type"),
    REMOTO=job.get("detected_extensions", {}).get("work_from_home"),
    QUALIFICACOES=get_qualificacoes(job),
    RESPONSABILIDADES=get_responsabilidades(job),
    BENEFICIOS=get_beneficios(job),
)

# -----------------------------------------------------------------------------
# Função para tratar os resultados e gerar uma lista de registros de vagas
# -----------------------------------------------------------------------------


def trata_resultados(resultados: List[Dict]) -> List[RegistroVaga]:
    return reduce(
        lambda resultados_tratados, resultado: resultados_tratados
        + [gera_registro(resultado)],
        resultados,
        [],
    )


# -----------------------------------------------------------------------------
# Função para gerar um DataFrame a partir dos resultados tratados
# -----------------------------------------------------------------------------


def gera_df_resultados(resultados_tratados: List[RegistroVaga]) -> DataFrame:
    df = DataFrame([res.model_dump() for res in resultados_tratados])
    df["REMOTO"] = df["REMOTO"].astype(str)
    return df


# -----------------------------------------------------------------------------
# Função para gerar um DataFrame a partir dos resultados brutos
# -----------------------------------------------------------------------------


def df_resultados(resultados: List[Dict]) -> DataFrame:
    return gera_df_resultados(trata_resultados(resultados))


# -----------------------------------------------------------------------------
# Obtém os parâmetros da API a partir do arquivo de configuração
# -----------------------------------------------------------------------------


def get_parametros_busca(
    chave: str, api_key: str = API_SERPAPI
) -> Dict[str, str]:
    if not api_key:
        raise ValueError(
            "get_parametros_busca: 💀 ERRO! FORNEÇA A CHAVE DA API!"
        )

    # Carregando as configs
    with open(file=PATH_PARAMETROS_BUSCAS, mode="r", encoding="utf-8") as file:
        parametros_buscas = yaml.safe_load(file)
    parametros = parametros_buscas.get(chave)

    if parametros:
        parametros["api_key"] = api_key
        return parametros

    raise ValueError(
        f"get_parametros_busca: 💀 ERRO! Configuração '{chave}' não encontrada!"
    )
