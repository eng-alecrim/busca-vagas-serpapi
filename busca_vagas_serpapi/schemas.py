from typing import Optional

from pydantic import BaseModel


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
    start: Optional[str] = (
        None  # result offset (0 -> 1a pag, 10 -> 2a pag, 20 -> 3a pag, . . .)
    )

    # Advanced Google Jobs Parameters
    lrad: Optional[str] = None  # search radius in kilometers
    ltype: Optional[str] = None  # filter the results by work from home


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
