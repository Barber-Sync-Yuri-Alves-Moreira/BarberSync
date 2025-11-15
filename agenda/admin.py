from django.contrib import admin
from datetime import timedelta 
from .models import Barbeiros, Servicos, HorariosDisponiveis, Agendamentos
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin 
from django.utils import timezone 
class CustomAdminMedia:
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',) 
        }

class ServicosInline(admin.TabularInline):
    model = Servicos
    extra = 1 
    fields = ('nome', 'duracao_minutos', 'preco') 

class HorariosDisponiveisInline(admin.TabularInline):
    model = HorariosDisponiveis
    extra = 1 
    fields = ('data_hora', 'disponivel')
class BarbeirosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'descricao') 
    actions = None  # Remove o campo "Ir"
    inlines = [ServicosInline, HorariosDisponiveisInline] 
    
    class Media(CustomAdminMedia.Media):
        pass

class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone_cliente', 'servico', 'get_barbeiro_nome', 'get_data_hora')
    readonly_fields = ('horario',) 
    list_filter = ('horario__id_barbeiro', 'horario__data_hora') 
    actions = None  
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today = timezone.now().date() 
        return qs.filter(horario__data_hora__date__gte=today)
    def delete_model(self, request, obj):
        horario = obj.horario
        horario.disponivel = True 
        horario.save()            
        obj.delete() 
        self.message_user(request, "Agendamento cancelado e horário liberado com sucesso.")

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

class CustomUserAdmin(UserAdmin):
    search_fields = ()
    list_filter = ()
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    actions = None 
    
    class Media(CustomAdminMedia.Media):
        pass
admin.site.unregister(User)
admin.site.register(Barbeiros, BarbeirosAdmin)
admin.site.register(Agendamentos, AgendamentosAdmin)
admin.site.register(User, CustomUserAdmin)