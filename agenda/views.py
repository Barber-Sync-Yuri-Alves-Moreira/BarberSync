from django.shortcuts import render, get_object_or_404, redirect
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis, Agendamentos
from django.utils import timezone
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.contrib import messages

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
        data_hora__gte=agora,
        disponivel=True
    )

    datas_disponiveis = horarios_futuros.annotate(data=TruncDate('data_hora')).values('data').distinct().order_by('data')

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

    horarios_do_dia_objs = HorariosDisponiveis.objects.filter(
        id_barbeiro=barbeiro,
        data_hora__date=data_selecionada,
        data_hora__gte=agora,
        disponivel=True
    ).order_by('data_hora')

    horarios_com_ids = []
    for horario_obj in horarios_do_dia_objs:
        hora_utc = horario_obj.data_hora
        hora_ajustada = hora_utc - timedelta(hours=3)
        hora_formatada = hora_ajustada.strftime('%H:%M')

        horarios_com_ids.append({
            'id': horario_obj.id,
            'hora_str': hora_formatada
        })

    context = {
        'barbeiro': barbeiro,
        'servico': servico,
        'data_selecionada': data_selecionada,
        'horarios': horarios_com_ids
    }
    return render(request, 'agenda/selecionar_horario.html', context)

def dados_cliente(request, barbeiro_id, servico_id, horario_id):

    horario_obj = get_object_or_404(HorariosDisponiveis, id=horario_id)

    if not horario_obj.disponivel:
        messages.error(request, "Este horário não está mais disponível. Por favor, selecione outro.")
        data_str = horario_obj.data_hora.strftime('%Y-%m-%d')
        return redirect('selecionar_horario', barbeiro_id=barbeiro_id, servico_id=servico_id, data=data_str)

    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        telefone_cliente = request.POST.get('telefone_cliente')
        cpf_cliente = request.POST.get('cpf_cliente')

        servico = get_object_or_404(Servicos, id=servico_id)

        try:
            novo_agendamento = Agendamentos.objects.create(
                nome_cliente=nome_cliente,
                telefone_cliente=telefone_cliente,
                cpf_cliente=cpf_cliente,
                servico=servico,
                horario=horario_obj
            )

            horario_obj.disponivel = False
            horario_obj.save()

            messages.success(request, f"Agendamento realizado com sucesso!")

            return redirect('confirmacao', agendamento_id=novo_agendamento.id)

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao salvar o agendamento: {e}")
            return redirect('lista_barbeiros')

    context = {
        'barbeiro_id': barbeiro_id,
        'servico_id': servico_id,
        'horario_id': horario_id,
        'horario': horario_obj,
        'barbeiro': get_object_or_404(Barbeiros, id=barbeiro_id),
        'servico': get_object_or_404(Servicos, id=servico_id),
    }
    return render(request, 'agenda/dados_cliente.html', context)

def confirmacao(request, agendamento_id):

    agendamento = get_object_or_404(Agendamentos, id=agendamento_id)

    barbeiro = agendamento.horario.id_barbeiro
    servico = agendamento.servico

    context = {
        'agendamento': agendamento,
        'barbeiro': barbeiro,
        'servico': servico,
        'data_hora_agendada': agendamento.horario.data_hora - timedelta(hours=3)
    }

    return render(request, 'agenda/confirmacao.html', context)
