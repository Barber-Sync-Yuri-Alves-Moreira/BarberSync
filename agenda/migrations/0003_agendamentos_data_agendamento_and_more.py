
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_alter_horariosdisponiveis_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentos',
            name='data_agendamento',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='cpf_cliente',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='horario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='agenda.horariosdisponiveis', verbose_name='Horário Reservado'),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='nome_cliente',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='agendamentos',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='agenda.servicos', verbose_name='Serviço Agendado'),
        ),
    ]
