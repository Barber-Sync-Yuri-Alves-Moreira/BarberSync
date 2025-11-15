from django.db import models
from django.conf import settings
class Barbeiros(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='barbeiros/', null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Barbeiro"
        verbose_name_plural = "Barbeiros"

    def __str__(self):
        return self.nome
class Servicos(models.Model):
    barbeiro = models.ForeignKey(
        Barbeiros, 
        on_delete=models.CASCADE, 
        related_name="servicos" 
    )
    nome = models.CharField(max_length=100)
    duracao_minutos = models.IntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return f"{self.nome} - {self.barbeiro.nome}"
class HorariosDisponiveis(models.Model):
    id_barbeiro = models.ForeignKey(
        Barbeiros, 
        on_delete=models.CASCADE,
        related_name="horarios"
    )
    data_hora = models.DateTimeField()
    disponivel = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        unique_together = ('id_barbeiro', 'data_hora')

    def __str__(self):
        return f"{self.id_barbeiro.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
class Agendamentos(models.Model):
    nome_cliente = models.CharField(max_length=100)
    telefone_cliente = models.CharField(max_length=15)
    cpf_cliente = models.CharField(max_length=14, blank=True, null=True)
    servico = models.ForeignKey(Servicos, on_delete=models.PROTECT) 
    horario = models.OneToOneField(HorariosDisponiveis, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"{self.nome_cliente} - {self.horario.id_barbeiro.nome} - {self.horario.data_hora.strftime('%H:%M')}"