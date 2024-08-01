# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel

# =============================================================================
# SCHEMAS
# =============================================================================

# -----------------------------------------------------------------------------
# Classe básica para realizar um request para o SerpAPI
# -----------------------------------------------------------------------------


class BuscaVaga(BaseModel):
    # Serpapi Parameters
    api_key: str  # REQUIRED
    engine: str  # REQUIRED

    # Search Query
    q: str  # REQUIRED

    # Geographic Location
    location: Optional[str] = None  # where you want the search to originate

    # Localization
    google_domain: Optional[str] = None  # Google domain to use
    gl: Optional[str] = None  # the country to use for the Google search
    hl: Optional[str] = None  # the language to use for the Google Jobs search

    # Pagination
    next_page_token: Optional[str] = (
        None  # Parameter defines the next page token. It is used for retrieving the next page of results. Up to 10 results are returned per page.
    )

    # Advanced Google Jobs Parameters
    lrad: Optional[str] = None  # search radius in kilometers
    ltype: Optional[str] = None  # filter the results by work from home


# -----------------------------------------------------------------------------
# Ajudar em buscas múltiplas
# -----------------------------------------------------------------------------


class FilaBuscas(BaseModel):
    buscas: List[BuscaVaga]  # Lista de buscas a serem feitas
    nomeArquivo: str  # Nome do arquivo empilhado
    diretorioDestino: Union[Path, str]  # Diretório onde será salvo

    def get_busca(self) -> BuscaVaga:
        return self.buscas.pop(0)

    def add_busca(self, busca: BuscaVaga) -> None:
        self.buscas += [busca]
        return None

    def remove_busca(self, busca) -> None:
        self.buscas.remove(busca)
        return None


# -----------------------------------------------------------------------------
# Estrutura das informações que serão extraídas da busca -> gerar uma tabela
# -----------------------------------------------------------------------------


class RegistroVaga(BaseModel):
    ID_VAGA: str
    DATA_CONSULTA: str
    TITULO: str
    EMPRESA: str
    LOCAL: str
    ANUNCIANTE: str
    DESCRICAO: str
    POSTADO_EM: Optional[str] = None
    REGIME: Optional[str] = None
    REMOTO: Optional[bool] = None
    QUALIFICACOES: Optional[str] = None
    RESPONSABILIDADES: Optional[str] = None
    BENEFICIOS: Optional[str] = None
