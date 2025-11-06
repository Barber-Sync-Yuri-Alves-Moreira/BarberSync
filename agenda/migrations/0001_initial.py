
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barbeiros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='barbeiros/')),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Barbeiro',
                'verbose_name_plural': 'Barbeiros',
            },
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('duracao_minutos', models.IntegerField(help_text='Duração do serviço em minutos')),
                ('preco', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
            },
        ),
        migrations.CreateModel(
            name='HorariosDisponiveis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(verbose_name='Data e Hora')),
                ('disponivel', models.BooleanField(default=True, verbose_name='Disponível')),
                ('id_barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.barbeiros', verbose_name='Barbeiro')),
            ],
            options={
                'verbose_name': 'Horário Disponível',
                'verbose_name_plural': 'Horários Disponíveis',
                'ordering': ['id_barbeiro', 'data_hora'],
                'unique_together': {('id_barbeiro', 'data_hora')},
            },
        ),
        migrations.CreateModel(
            name='Agendamentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cliente', models.CharField(max_length=200, verbose_name='Nome do Cliente')),
                ('telefone_cliente', models.CharField(max_length=20, verbose_name='Telefone do Cliente')),
                ('cpf_cliente', models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF (Opcional)')),
                ('horario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agendamento', to='agenda.horariosdisponiveis')),
                ('servico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agenda.servicos', verbose_name='Serviço')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
            },
        ),
        migrations.CreateModel(
            name='BarbeirosServicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_barbeiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.barbeiros', verbose_name='Barbeiro')),
                ('id_servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.servicos', verbose_name='Serviço')),
            ],
            options={
                'verbose_name': 'Serviço do Barbeiro',
                'verbose_name_plural': 'Serviços dos Barbeiros',
                'unique_together': {('id_barbeiro', 'id_servico')},
            },
        ),
    ]
