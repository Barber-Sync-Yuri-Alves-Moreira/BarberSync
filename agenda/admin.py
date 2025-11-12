from django.contrib import admin
from datetime import timedelta 
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis, Agendamentos

class CustomAdminMedia:
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',) 
        }

class BarbeirosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'descricao') 
    search_fields = ('nome',) 
    actions = None
    
    class Media(CustomAdminMedia.Media):
        pass

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)
    list_filter = ('duracao_minutos', 'preco') 
    actions = None
    
    class Media(CustomAdminMedia.Media):
        pass

class BarbeirosServicosAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'get_servico_nome') 
    list_filter = ('id_barbeiro', 'id_servico') 
    actions = None

    class Media(CustomAdminMedia.Media):
        pass
    
    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro' 

    def get_servico_nome(self, obj):
        return obj.id_servico.nome
    get_servico_nome.short_description = 'Serviço' 

class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'get_data_hora_com_gambiarra', 'disponivel') 
    list_filter = ('id_barbeiro', 'data_hora', 'disponivel') 
    list_editable = ('disponivel',) 
    actions = None

    class Media(CustomAdminMedia.Media):
        pass

    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro'

    def get_data_hora_com_gambiarra(self, obj):
        if obj.data_hora is None:
            return "N/A"
        
        data_hora_local = obj.data_hora - timedelta(hours=3)
        return data_hora_local.strftime('%d/%m/%Y %H:%M')
    
    get_data_hora_com_gambiarra.short_description = 'Data e Hora' 
    get_data_hora_com_gambiarra.admin_order_field = 'data_hora'


class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone_cliente', 'servico', 'get_barbeiro_nome', 'get_data_hora')
    search_fields = ('nome_cliente', 'telefone_cliente', 'cpf_cliente')
    list_filter = ('horario__id_barbeiro', 'horario__data_hora')
    readonly_fields = ('horario',) 
    actions = None
    
    class Media(CustomAdminMedia.Media):
        pass

    def get_barbeiro_nome(self, obj):
        return obj.horario.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro'
    get_barbeiro_nome.admin_order_field = 'horario__id_barbeiro__nome'

    def get_data_hora(self, obj):
        if obj.horario.data_hora is None:
            return "N/A"
        
        data_hora_local = obj.horario.data_hora - timedelta(hours=3)
        return data_hora_local.strftime('%d/%m/%Y %H:%M')
    
    get_data_hora.short_description = 'Data e Hora'
    get_data_hora.admin_order_field = 'horario__data_hora'
    
    
admin.site.register(Barbeiros, BarbeirosAdmin)
admin.site.register(Servicos, ServicosAdmin)
admin.site.register(BarbeirosServicos, BarbeirosServicosAdmin)
admin.site.register(HorariosDisponiveis, HorariosDisponiveisAdmin)
admin.site.register(Agendamentos, AgendamentosAdmin)