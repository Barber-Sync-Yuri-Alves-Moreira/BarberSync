

from django.db import models

class Barbearias(models.Model):
    nome_negocio = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    senha_hash = models.CharField(max_length=255)
    whatsapp_negocio = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_negocio

    class Meta:
        db_table = 'barbearias'
        verbose_name_plural = "Barbearias"


class Barbeiros(models.Model):
    id_barbearia = models.ForeignKey(
        Barbearias, 
        on_delete=models.CASCADE, 
        db_column='id_barbearia',
        verbose_name="Barbearias"
    )
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='barbeiros/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'barbeiros'
        verbose_name_plural = "Barbeiros"


class Servicos(models.Model):
    id_barbearia = models.ForeignKey(
        Barbearias, 
        on_delete=models.CASCADE, 
        db_column='id_barbearia',
        verbose_name="Barbearia"
    )
    nome = models.CharField(max_length=100)
    duracao_minutos = models.IntegerField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'servicos'
        verbose_name_plural = "Serviços"


class BarbeirosServicos(models.Model):
    id_barbeiro = models.ForeignKey(
        Barbeiros, 
        on_delete=models.CASCADE, 
        db_column='id_barbeiro',
        verbose_name="Barbeiro"
    )
    id_servico = models.ForeignKey(
        Servicos, 
        on_delete=models.CASCADE, 
        db_column='id_servico',
        verbose_name="Serviço"
    )


    def __str__(self):

        return f"{self.id_servico.nome} - {self.id_barbeiro.nome}"


    class Meta:
        db_table = 'barbeiros_servicos'
        unique_together = (('id_barbeiro', 'id_servico'),)
        verbose_name_plural = "Relação Barbeiro-Serviço"


class HorariosDisponiveis(models.Model):
    id_barbeiro = models.ForeignKey(
        Barbeiros, 
        on_delete=models.CASCADE, 
        db_column='id_barbeiro',
        verbose_name="Barbeiro"
    )
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.id_barbeiro.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        db_table = 'horarios_disponiveis'
        unique_together = (('id_barbeiro', 'data_hora'),)
        verbose_name_plural = "Horários Disponíveis"