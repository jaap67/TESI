from django.db import models

class Question03(models.Model):
    localidade = models.CharField(max_length=255, null=True)
    temperatura = models.CharField(max_length=255, null=True)
    condicao = models.CharField(max_length=255, null=True)
    sensacao = models.CharField(max_length=255, null=True)
    humidade = models.CharField(max_length=255, null=True)
    pressao = models.CharField(max_length=255, null=True)
    vento = models.CharField(max_length=255, null=True)
    atualizacao = models.CharField(max_length=255, null=True)
    