# busca-vagas-serpapi

> This project is licensed under the terms of the GNU General Public License v3.0 license.

## Guia de uso

### Exemplo 1: Busca única

``` python
from busca_vagas_serpapi.schemas import BuscaVaga
from busca_vagas_serpapi.busca_vagas import loop_busca
from busca_vagas_serpapi.utils_vagas import df_resultados

minha_busca = BuscaVaga(
    api_key="****************************************************************",
    engine="google_jobs",
    q="Cientista de Dados",
    google_domain="google.com.br",
    location="Brazil",
    gl="br",
    hl="pt"
)

resultados = loop_busca(minha_busca)
resultados_tratados = df_resultados(resultados)
```

### Exemplo 2: Múltiplas buscas

``` python
from busca_vagas_serpapi.fila_buscas import pesquisa_fila
from busca_vagas_serpapi.schemas import BuscaVaga, FilaBuscas

CONFIG_BASICA = {
    "api_key": "****************************************************************",
    "engine": "google_jobs",
    "google_domain": "google.com.br",
    "location": "Brazil",
    "gl": "br",
    "hl": "pt",
}

busca_1 = BuscaVaga(q="Cientista de Dados", **CONFIG_BASICA)

busca_2 = BuscaVaga(q="Engenheiro de Dados", **CONFIG_BASICA)

busca_3 = BuscaVaga(q="Engenheiro de Machine Learning", **CONFIG_BASICA)

fila_buscas = FilaBuscas(
    buscas=[busca_1, busca_2, busca_3],
    nomeArquivo="profissoes_dados",
    diretorioDestino="./data/bronze",
)

pesquisa_fila(fila_buscas)
```
