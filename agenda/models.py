from django.db import models

class Barbeiros(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='barbeiros/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nome
        
    class Meta:
        verbose_name = "Barbeiro"
        verbose_name_plural = "Barbeiros"

class Servicos(models.Model):
    nome = models.CharField(max_length=100)
    duracao_minutos = models.IntegerField(help_text="Duração do serviço em minutos")
    preco = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.nome
        
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

class BarbeirosServicos(models.Model):
    id_barbeiro = models.ForeignKey(Barbeiros, on_delete=models.CASCADE, verbose_name="Barbeiro")
    id_servico = models.ForeignKey(Servicos, on_delete=models.CASCADE, verbose_name="Serviço")
    
    def __str__(self):
        barbeiro_nome = self.id_barbeiro.nome if self.id_barbeiro else 'ID ' + str(self.id_barbeiro_id)
        servico_nome = self.id_servico.nome if self.id_servico else 'ID ' + str(self.id_servico_id)
        return f"{barbeiro_nome} - {servico_nome}"
        
    class Meta:
        verbose_name = "Serviço do Barbeiro"
        verbose_name_plural = "Serviços dos Barbeiros"
        unique_together = ('id_barbeiro', 'id_servico')

class HorariosDisponiveis(models.Model):
    id_barbeiro = models.ForeignKey(Barbeiros, on_delete=models.CASCADE, verbose_name="Barbeiro")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    
    def __str__(self):
        barbeiro_nome = self.id_barbeiro.nome if self.id_barbeiro else 'ID ' + str(self.id_barbeiro_id)
        data_hora_formatada = self.data_hora.strftime('%d/%m/%Y %H:%M') if self.data_hora else 'Data/Hora inválida'
        return f"{barbeiro_nome} - {data_hora_formatada}"
        
    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        unique_together = ('id_barbeiro', 'data_hora')
        ordering = ['id_barbeiro', 'data_hora'] 