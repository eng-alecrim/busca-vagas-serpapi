import re
from datetime import datetime, timedelta, timezone
from typing import Optional


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
