from typing import Dict, List, Optional

from serpapi import GoogleSearch

from busca_vagas_serpapi.schemas import BuscaVaga


def faz_busca(busca: BuscaVaga) -> Dict:
    search = GoogleSearch(busca.model_dump())
    results = search.get_dict()

    return results


def resultados_busca(results: Dict) -> Optional[List[Dict]]:
    if "error" in results.keys():
        print(results.get("error"))
        return None

    data_criacao = results.get("search_metadata", {}).get("created_at")
    assert data_criacao is not None, "data_criacao is None"

    jobs = results.get("jobs_results")
    assert jobs is not None, "jobs is None"

    def add_data_criacao(job: Dict) -> Dict:
        job["created_at"] = data_criacao
        return job

    return list(map(add_data_criacao, jobs))


def loop_busca(busca: BuscaVaga) -> Optional[List[Dict]]:
    pagina = 0
    todas_vagas = []

    while True:
        busca.start = str(10 * pagina)
        vagas = resultados_busca(faz_busca(busca))
        if vagas is None:
            break
        print(f"Página {pagina + 1}: {len(vagas)} resultado(s) encontrados.")
        todas_vagas += vagas
        pagina += 1

    print(f"\nForam encontradas {len(todas_vagas)} vaga(s)!")

    return todas_vagas
