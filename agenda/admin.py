from django.contrib import admin
from datetime import timedelta # CORREÇÃO: Importação para usar timedelta
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis, Agendamentos

# Definição da classe Media para injeção de CSS personalizado
class CustomAdminMedia:
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',) # Certifique-se que o arquivo CSS existe neste caminho
        }

class BarbeirosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'descricao') 
    search_fields = ('nome',) 
    
    # --- LIMPEZA: Remove o dropdown de ações em massa ---
    actions = None
    
    # --- ESTILO: Injeta o CSS personalizado ---
    class Media(CustomAdminMedia.Media):
        pass

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)
    list_filter = ('duracao_minutos', 'preco') 
    
    # --- LIMPEZA: Remove o dropdown de ações em massa ---
    actions = None
    
    # --- ESTILO: Injeta o CSS personalizado ---
    class Media(CustomAdminMedia.Media):
        pass

class BarbeirosServicosAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'get_servico_nome') 
    list_filter = ('id_barbeiro', 'id_servico') 
    
    # --- LIMPEZA: Remove o dropdown de ações em massa ---
    actions = None
    
    # --- ESTILO: Injeta o CSS personalizado ---
    class Media(CustomAdminMedia.Media):
        pass
    
    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro' 

    def get_servico_nome(self, obj):
        return obj.id_servico.nome
    get_servico_nome.short_description = 'Serviço' 

class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'data_hora', 'disponivel') 
    list_filter = ('id_barbeiro', 'data_hora', 'disponivel') 
    list_editable = ('disponivel',) 
    
    # --- LIMPEZA: Remove o dropdown de ações em massa ---
    actions = None
    
    # --- ESTILO: Injeta o CSS personalizado ---
    class Media(CustomAdminMedia.Media):
        pass

    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro'

class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone_cliente', 'servico', 'get_barbeiro_nome', 'get_data_hora')
    search_fields = ('nome_cliente', 'telefone_cliente', 'cpf_cliente')
    list_filter = ('horario__id_barbeiro', 'horario__data_hora')
    readonly_fields = ('horario',) 
    
    # --- LIMPEZA: Remove o dropdown de ações em massa ---
    actions = None
    
    # --- ESTILO: Injeta o CSS personalizado ---
    class Media(CustomAdminMedia.Media):
        pass

    def get_barbeiro_nome(self, obj):
        return obj.horario.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro'
    get_barbeiro_nome.admin_order_field = 'horario__id_barbeiro__nome'

    # CORREÇÃO: Aplica o timedelta e formata
    def get_data_hora(self, obj):
        # Data de hora corrigida para fuso
        data_hora_local = obj.horario.data_hora - timedelta(hours=3)
        return data_hora_local.strftime('%d/%m/%Y %H:%M')
    get_data_hora.short_description = 'Data e Hora'
    get_data_hora.admin_order_field = 'horario__data_hora'
    
    
# Registro dos modelos
admin.site.register(Barbeiros, BarbeirosAdmin)
admin.site.register(Servicos, ServicosAdmin)
admin.site.register(BarbeirosServicos, BarbeirosServicosAdmin)
admin.site.register(HorariosDisponiveis, HorariosDisponiveisAdmin)
admin.site.register(Agendamentos, AgendamentosAdmin)