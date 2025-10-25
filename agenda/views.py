from django.shortcuts import render, get_object_or_404
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis
from django.utils import timezone
from django.db.models.functions import TruncDate 
from datetime import datetime 

def lista_barbeiros(request):
    barbeiros = Barbeiros.objects.all()
    context = {'barbeiros': barbeiros}
    return render(request, 'agenda/lista_barbeiros.html', context)

def lista_servicos(request, barbeiro_id):
    barbeiro = get_object_or_404(Barbeiros, id=barbeiro_id)
    servicos_ids = BarbeirosServicos.objects.filter(id_barbeiro=barbeiro).values_list('id_servico', flat=True)
    servicos = Servicos.objects.filter(id__in=servicos_ids)
    
    context = {
        'barbeiro': barbeiro,
        'servicos': servicos
    }
    return render(request, 'agenda/lista_servicos.html', context)

def selecionar_data(request, barbeiro_id, servico_id):
    barbeiro = get_object_or_404(Barbeiros, id=barbeiro_id)
    servico = get_object_or_404(Servicos, id=servico_id)
    
    agora = timezone.now()
    

    horarios_futuros = HorariosDisponiveis.objects.filter(
        id_barbeiro=barbeiro,
        data_hora__gte=agora
    )
    
    datas_disponiveis = horarios_futuros.annotate(
        data=TruncDate('data_hora')
    ).values('data').distinct().order_by('data')

    context = {
        'barbeiro': barbeiro,
        'servico': servico,
        'datas': datas_disponiveis 
    }
    return render(request, 'agenda/selecionar_data.html', context)

def selecionar_horario(request, barbeiro_id, servico_id, data):
    barbeiro = get_object_or_404(Barbeiros, id=barbeiro_id)
    servico = get_object_or_404(Servicos, id=servico_id)
    

    data_selecionada = datetime.strptime(data, '%Y-%m-%d').date()
    
    agora = timezone.now()

    horarios_do_dia = HorariosDisponiveis.objects.filter(
        id_barbeiro=barbeiro,
        data_hora__date=data_selecionada, 
        data_hora__gte=agora 
    ).order_by('data_hora')

    context = {
        'barbeiro': barbeiro,
        'servico': servico,
        'data_selecionada': data_selecionada,
        'horarios': horarios_do_dia
    }
    return render(request, 'agenda/selecionar_horario.html', context)