
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horariosdisponiveis',
            options={'verbose_name': 'Horário Disponível', 'verbose_name_plural': 'Horários Disponíveis'},
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='horario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='agenda.horariosdisponiveis', verbose_name='Horário Agendado'),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='nome_cliente',
            field=models.CharField(help_text='Nome completo do cliente', max_length=100),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='servico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='agenda.servicos', verbose_name='Serviço'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='telefone_cliente',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='servicos',
            name='preco',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
