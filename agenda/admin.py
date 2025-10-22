

from django.contrib import admin
from .models import Barbearias, Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis 

class BarbeariasAdmin(admin.ModelAdmin):
    exclude = ('senha_hash',) 


    actions = None 


class BarbeirosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'id_barbearia', 'imagem')
    list_filter = ('id_barbearia',)
    actions = None

class BarbeirosServicosAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'get_servico_nome') 
    list_filter = ('id_barbeiro', 'id_servico')
    actions = None 

    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro' 

    def get_servico_nome(self, obj):
        return obj.id_servico.nome
    get_servico_nome.short_description = 'Serviço' 

class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('id_barbeiro', 'data_hora')
    list_filter = ('id_barbeiro', 'data_hora')
    actions = None 


admin.site.register(Barbearias, BarbeariasAdmin)
admin.site.register(Barbeiros, BarbeirosAdmin)
admin.site.register(Servicos) 
admin.site.register(BarbeirosServicos, BarbeirosServicosAdmin) 
admin.site.register(HorariosDisponiveis, HorariosDisponiveisAdmin)