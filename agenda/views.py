from django.shortcuts import render, get_object_or_404, redirect
from .models import Barbeiros, Servicos, HorariosDisponiveis, Agendamentos
from django.utils import timezone
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.contrib import messages
import re 
from urllib.parse import quote 

# --- Função de Validação de CPF ---
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    return True

# --- View: lista_barbeiros ---
def lista_barbeiros(request):
    barbeiros = Barbeiros.objects.all()
    context = {'barbeiros': barbeiros}
    return render(request, 'agenda/lista_barbeiros.html', context)
def lista_servicos(request, barbeiro_id):
    barbeiro = get_object_or_404(Barbeiros, id=barbeiro_id)
    servicos = Servicos.objects.filter(barbeiro=barbeiro)



    context = {
        'barbeiro': barbeiro,
        'servicos': servicos
    }
    return render(request, 'agenda/lista_servicos.html', context)

# --- View: selecionar_data ---
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

# --- View: selecionar_horario ---
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

# --- View: dados_cliente ---
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
        if not validar_cpf(cpf_cliente):
            messages.error(request, "CPF inválido. Por favor, verifique os dados.")
            horario_corrigido = get_object_or_404(HorariosDisponiveis, id=horario_id)
            if horario_corrigido.data_hora:
                 horario_corrigido.data_hora = horario_corrigido.data_hora - timedelta(hours=3) # Gambiarra -3h
            context = {
                'barbeiro_id': barbeiro_id, 'servico_id': servico_id, 'horario_id': horario_id,
                'horario': horario_corrigido,
                'barbeiro': get_object_or_404(Barbeiros, id=barbeiro_id),
                'servico': get_object_or_404(Servicos, id=servico_id),
                'form_data': request.POST
            }
            return render(request, 'agenda/dados_cliente.html', context)
        servico = get_object_or_404(Servicos, id=servico_id)
        try:
            horario_original_para_salvar = get_object_or_404(HorariosDisponiveis, id=horario_id)
            novo_agendamento = Agendamentos.objects.create(
                nome_cliente=nome_cliente,
                telefone_cliente=telefone_cliente,
                cpf_cliente=cpf_cliente, 
                servico=servico,
                horario=horario_original_para_salvar 
            )
            horario_original_para_salvar.disponivel = False
            horario_original_para_salvar.save()
            messages.success(request, f"Agendamento realizado com sucesso!")
            return redirect('confirmacao', agendamento_id=novo_agendamento.id)
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao salvar o agendamento: {e}")
            return redirect('lista_barbeiros')

    if horario_obj.data_hora:
        horario_obj.data_hora = horario_obj.data_hora - timedelta(hours=3) 

    context = {
        'barbeiro_id': barbeiro_id,
        'servico_id': servico_id,
        'horario_id': horario_id,
        'horario': horario_obj, 
        'barbeiro': get_object_or_404(Barbeiros, id=barbeiro_id),
        'servico': get_object_or_404(Servicos, id=servico_id),
    }
    return render(request, 'agenda/dados_cliente.html', context)

# --- View: confirmacao ---
def confirmacao(request, agendamento_id):
    agendamento = get_object_or_404(Agendamentos, id=agendamento_id)
    barbeiro = agendamento.horario.id_barbeiro
    servico = agendamento.servico
    data_hora_agendada_utc = agendamento.horario.data_hora
    base_url = "https://api.whatsapp.com/send?phone=5575988728766"
    local_tz = timezone.get_current_timezone() 
    data_hora_local_para_msg = data_hora_agendada_utc.astimezone(local_tz) 
    raw_message = (
        f"Olá! Gostaria de confirmar meu agendamento:\n\n"
        f"*Barbeiro:* {barbeiro.nome}\n"
        f"*Serviço:* {servico.nome}\n"
        f"*Data:* {data_hora_local_para_msg.strftime('%d/%m/%Y')}\n"
        f"*Horário:* {data_hora_local_para_msg.strftime('%H:%M')}"
    )
    encoded_message = quote(raw_message)
    whatsapp_link_final = f"{base_url}&text={encoded_message}"

    context = {
        'agendamento': agendamento,
        'barbeiro': barbeiro,
        'servico': servico,
        'data_hora_agendada': data_hora_agendada_utc, 
        'whatsapp_link': whatsapp_link_final
    }
    return render(request, 'agenda/confirmacao.html', context)