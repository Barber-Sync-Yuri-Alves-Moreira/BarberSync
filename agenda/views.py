from django.shortcuts import render, get_object_or_404
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis
from django.utils import timezone
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta # Import timedelta

# views lista_barbeiros, lista_servicos, selecionar_data continuam iguais...

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

# --- VIEW MODIFICADA ---
def selecionar_horario(request, barbeiro_id, servico_id, data):
    barbeiro = get_object_or_404(Barbeiros, id=barbeiro_id)
    servico = get_object_or_404(Servicos, id=servico_id)
    data_selecionada = datetime.strptime(data, '%Y-%m-%d').date()
    agora = timezone.now()

    horarios_do_dia_objs = HorariosDisponiveis.objects.filter(
        id_barbeiro=barbeiro,
        data_hora__date=data_selecionada,
        data_hora__gte=agora
    ).order_by('data_hora')

    # --- AJUSTE MANUAL AQUI ---
    horarios_ajustados = []
    for horario_obj in horarios_do_dia_objs:
        # Pega a hora UTC do banco
        hora_utc = horario_obj.data_hora
        # Subtrai 3 horas manualmente
        hora_ajustada = hora_utc - timedelta(hours=3)
        # Formata como HH:MM
        hora_formatada = hora_ajustada.strftime('%H:%M')
        # Guarda a string formatada na nova lista
        horarios_ajustados.append(hora_formatada)
    # --- FIM DO AJUSTE MANUAL ---

    context = {
        'barbeiro': barbeiro,
        'servico': servico,
        'data_selecionada': data_selecionada,
        'horarios': horarios_ajustados # Envia a lista de strings HH:MM
    }
    return render(request, 'agenda/selecionar_horario.html', context)