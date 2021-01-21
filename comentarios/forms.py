from typing import Any, Dict
from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):
    def clean(self) -> Dict[str, Any]:
        data = self.cleaned_data
        # nome = data.get('nome')
        # email = data.get('email')
        conteudo = data.get('conteudo')

        # if nome == 'Tiago':
        #     self.add_error('nome', 'Esse usuario nao pode cementar!')

        if any(palavrao in conteudo for palavrao in ['shit', 'merda', 'cacete']):
            self.add_error('conteudo', 'Conteudo invalido!')

        return data

    class Meta:
        model = Comentario
        fields = ('nome', 'email', 'conteudo')
