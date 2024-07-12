# busca-vagas-serpapi

## Guia de uso

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
