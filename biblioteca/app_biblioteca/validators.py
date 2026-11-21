from datetime import date
from django.core.exceptions import ValidationError

def ValidarAnoPublicacao(valor):
    ano_atual = date.today().year
    if valor < 1450 or valor >ano_atual:
        raise ValidationError(f'O ano de publicação deve estar entre 1450 e o {ano_atual}')

def ValidarTamanhoCapa(file):
    limite =2
    if file.size > limite*1024*1024:
        raise ValidationError(f'O tamanho do arquivo deve ter no maximo {limite}mb')
