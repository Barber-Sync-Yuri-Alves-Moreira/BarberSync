

from django.shortcuts import render
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis



def lista_barbeiros(request):

    todos_os_barbeiros = Barbeiros.objects.all()


    contexto = {
        'barbeiros': todos_os_barbeiros
    }
    return render(request, 'agenda/lista_barbeiros.html', contexto)



#
def lista_servicos(request, barbeiro_id):

    barbeiro_selecionado = Barbeiros.objects.get(id=barbeiro_id)


    relacoes = BarbeirosServicos.objects.filter(id_barbeiro=barbeiro_selecionado)

   
    servicos_do_barbeiro = [relacao.id_servico for relacao in relacoes]

    contexto = {
        'barbeiro': barbeiro_selecionado,
        'servicos': servicos_do_barbeiro
    }
    return render(request, 'agenda/lista_servicos.html', contexto)