from datetime import date

from django.core.exceptions import ValidationError


def validar_ano_publicacao(value):
    ano_atual = date.today().year
    if value < 1450 or value > ano_atual:
        raise ValidationError(
            "O ano deve estar entre 1450 e %(ano_atual)s. Recebido: %(value)s",
            params={"ano_atual": ano_atual, "value": value},
        )


def validar_tamanho_arquivo(file):
    limit_mb = 1
    if file.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"O arquivo deve ter no máximo {limit_mb} MB.")
