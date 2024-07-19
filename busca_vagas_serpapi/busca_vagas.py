# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import logging
import logging.config
from typing import Dict, List, Optional

from serpapi import GoogleSearch

from busca_vagas_serpapi.schemas import BuscaVaga

# =============================================================================
# CONSTANTES
# =============================================================================

logging.config.fileConfig("config/logging.toml")
LOGGER = logging.getLogger("logMain.info.debug")

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Faz um request para a API da SerpAPI. O resultado é um Dict com 10 vagas máx
# -----------------------------------------------------------------------------


def faz_busca(busca: BuscaVaga) -> Dict:
    search = GoogleSearch(busca.model_dump())
    results = search.get_dict()

    return results


# -----------------------------------------------------------------------------
# Parsing do JSON de resposta. Uma List[Dict] com as vagas encontradas
# -----------------------------------------------------------------------------


def resultados_busca(results: Dict) -> Optional[List[Dict]]:
    if "error" in results.keys():
        erro = results.get("error", "")
        if "returned any results" in erro:
            return None
        LOGGER.warning(f"resultados_busca: WARNING! {erro}.")
        return None

    data_criacao = results.get("search_metadata", {}).get("created_at")
    assert data_criacao is not None, "resultados_busca: data_criacao is None"

    jobs = results.get("jobs_results")
    assert jobs is not None, "resultados_busca: jobs is None"

    def add_data_criacao(job: Dict) -> Dict:
        job["created_at"] = data_criacao
        return job

    return list(map(add_data_criacao, jobs))


# -----------------------------------------------------------------------------
# Uma busca traz, máx 10 vagas, porém podem haver mais. Esta função resolve isso.
# -----------------------------------------------------------------------------


def loop_busca(busca: BuscaVaga) -> Optional[List[Dict]]:
    pagina = 0
    todas_vagas = []

    LOGGER.info(f"loop_busca: Busca: '{busca.q}'.")

    while True:
        busca.start = str(10 * pagina)
        vagas = resultados_busca(faz_busca(busca))
        if vagas is None:
            break
        todas_vagas += vagas
        pagina += 1

    LOGGER.info(
        f"loop_busca: Busca: '{busca.q}' -> {len(todas_vagas)} vaga(s)."
    )

    return todas_vagas
