
from django.contrib import admin
from .models import Barbeiros, Servicos, BarbeirosServicos, HorariosDisponiveis 
class BarbeirosAdmin(admin.ModelAdmin):

    list_display = ('nome', 'imagem', 'descricao') 
    search_fields = ('nome',) 

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco')
    search_fields = ('nome',)
    list_filter = ('duracao_minutos', 'preco') 
class BarbeirosServicosAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'get_servico_nome') 
    list_filter = ('id_barbeiro', 'id_servico') 
    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro' 

    def get_servico_nome(self, obj):
        return obj.id_servico.nome
    get_servico_nome.short_description = 'Serviço' 


class HorariosDisponiveisAdmin(admin.ModelAdmin):
    list_display = ('get_barbeiro_nome', 'data_hora')
    list_filter = ('id_barbeiro', 'data_hora') 


    def get_barbeiro_nome(self, obj):
        return obj.id_barbeiro.nome
    get_barbeiro_nome.short_description = 'Barbeiro'


admin.site.register(Barbeiros, BarbeirosAdmin)
admin.site.register(Servicos, ServicosAdmin)
admin.site.register(BarbeirosServicos, BarbeirosServicosAdmin)
admin.site.register(HorariosDisponiveis, HorariosDisponiveisAdmin)


admin.site.site_header = "Painel Cleber Barbearia"
admin.site.site_title = "Admin Cleber Barbearia"
admin.site.index_title = "Gerenciamento"