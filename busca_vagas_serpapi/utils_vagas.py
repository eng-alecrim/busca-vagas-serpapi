# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from functools import reduce
from typing import Dict, List, Optional

from pandas import DataFrame

from busca_vagas_serpapi.schemas import RegistroVaga

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
