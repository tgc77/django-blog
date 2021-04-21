from typing import Any, Dict
from django.shortcuts import redirect, render
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models.query import QuerySet
from django.db.models import Q, Count, Case, When
from django.contrib import messages
from django.db import connection

from .models import Post
from comentarios.forms import FormComentario
from comentarios.models import Comentario


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado=True, then=1)
                )
            )
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        m_context = super().get_context_data(**kwargs)
        m_context['connection'] = connection
        return m_context


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')
        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )
        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    model = Post
    template_name = 'posts/post_detalhes.html'
    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado=True,
                                                post=post.id)
        contexto['comentarios'] = comentarios
        return contexto

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post = post

        if self.request.user.is_authenticated:
            comentario.usuario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentario enviado com sucesso!')

        return redirect('post_detalhes', pk=post.id)

# class PostDetalhes(View):
#     template_name = 'posts/post_detalhes.html'

#     def setup(self, request, *args, **kwargs):
#         super().setup(request, *args, **kwargs)

#         pk = self.kwargs.get('pk')
#         post = get_object_or_404(Post, pk=pk, publicado_post=True)
#         self.contexto = {
#             'post': post,
#             'comentarios': Comentario.objects.filter(post_comentario=post,
#                                                      publicado_comentario=True),
#             'form': FormComentario(request.POST or None),
#         }

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, self.contexto)

#     def post(self, request, *args, **kwargs):
#         form = self.contexto['form']

#         if not form.is_valid():
#             return render(request, self.template_name, self.contexto)

#         comentario = form.save(commit=False)

#         if request.user.is_authenticated:
#             comentario.usuario_comentario = request.user

#         comentario.post_comentario = self.contexto['post']
#         comentario.save()
#         messages.success(request, 'Seu comentário foi enviado para revisão.')
#         return redirect('post_detalhes', pk=self.kwargs.get('pk'))
