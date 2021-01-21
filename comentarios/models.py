from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from posts.models import Post


class Comentario(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField()
    conteudo = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    publicado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome
