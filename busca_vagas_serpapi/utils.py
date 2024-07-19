# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional, Union

from dotenv import find_dotenv, load_dotenv

# =============================================================================
# FUNÇÕES
# =============================================================================

load_dotenv(find_dotenv())
NOME_PROJETO = os.getenv("NOME_PROJETO", "")


def get_path_projeto(
    dir_atual: Path = Path.cwd(), nome_projeto: str = NOME_PROJETO
) -> Union[Callable, Path]:
    if not nome_projeto:
        raise ValueError("get_path_projeto: 💀 ERRO! nome_projeto deve ser fornecido!")
    if dir_atual.name == nome_projeto:
        return dir_atual

    return get_path_projeto(dir_atual.parent, nome_projeto)


# -----------------------------------------------------------------------------
# Transformar a data relativa em uma data absoluta
# -----------------------------------------------------------------------------


def get_data_postagem(data_consulta: Optional[str]) -> Optional[str]:
    def hora_exata_consulta() -> datetime:
        # Get the current date and time in UTC
        now_utc = datetime.now(timezone.utc)

        # Convert to a fixed UTC offset (e.g., UTC+03:00)
        fixed_utc_offset = -timedelta(hours=3)
        now_fixed_utc = now_utc.astimezone(timezone(fixed_utc_offset))

        return now_fixed_utc

    if data_consulta is None:
        return None

    f_get_numero = lambda regex, texto: (
        int(re.findall(regex, texto)[0]) if re.findall(regex, texto) else 0
    )

    n_horas = f_get_numero(r"[Hh]á (\d+) horas?", data_consulta)
    n_dias = f_get_numero(r"[Hh]á (\d+) dias?", data_consulta)
    n_meses = f_get_numero(r"[Hh]á (\d+) m[eê]s[es]?", data_consulta)
    n_semanas = f_get_numero(r"[Hh]á (\d+) semanas?", data_consulta)

    return (
        hora_exata_consulta()
        - timedelta(hours=n_horas, days=n_dias + 30 * n_meses, weeks=n_semanas)
    ).strftime("%Y-%m-%d")
