import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambiente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='nome do ambiente')),
                ('url', models.URLField(max_length=255, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'ambiente',
                'verbose_name_plural': 'ambientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('sigla', models.CharField(max_length=255, unique=True, verbose_name='sigla do campus')),
                ('token', models.CharField(max_length=255, verbose_name='token')),
                ('descricao', models.CharField(max_length=255, verbose_name='descrição')),
                ('url', models.URLField(max_length=255, verbose_name='URL')),
                ('thumbnail', models.ImageField(max_length=255, upload_to='', verbose_name='thumbnail')),
                ('active', models.BooleanField(verbose_name='ativo?')),
                ('homepage', models.BooleanField(default=True, verbose_name='listar na página principal?')),
            ],
            options={
                'verbose_name': 'campus',
                'verbose_name_plural': 'campi',
                'ordering': ['sigla'],
            },
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('sigla', models.CharField(max_length=255, unique=True, verbose_name='sigla do componente')),
                ('token', models.CharField(max_length=255, verbose_name='token')),
                ('descricao', models.CharField(max_length=255, verbose_name='descrição')),
                ('descricao_historico', models.CharField(max_length=255, verbose_name='descrição no histórico')),
                ('periodo', models.IntegerField(verbose_name='período')),
                ('tipo', models.IntegerField(verbose_name='tipo')),
                ('optativo', models.BooleanField(verbose_name='optativo')),
                ('qtd_avaliacoes', models.IntegerField(verbose_name='qtd. avalições')),
            ],
            options={
                'verbose_name': 'componente',
                'verbose_name_plural': 'componentes',
                'ordering': ['sigla'],
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('codigo', models.CharField(max_length=255, unique=True, verbose_name='código do curso')),
                ('nome', models.CharField(max_length=255, verbose_name='nome do curso')),
                ('descricao', models.CharField(max_length=255, verbose_name='descrição')),
                ('url_ppc', models.URLField(max_length=255, verbose_name='URL')),
                ('thumbnail', models.ImageField(max_length=255, upload_to='', verbose_name='thumbnail')),
                ('active', models.BooleanField(verbose_name='ativo?')),
                ('homepage', models.BooleanField(default=True, verbose_name='listar na página principal?')),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_mes', models.IntegerField(unique=True, verbose_name='ano.período')),
            ],
            options={
                'verbose_name': 'período',
                'verbose_name_plural': 'períodos',
                'ordering': ['ano_mes'],
            },
        ),
        migrations.CreateModel(
            name='Polo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='nome do pólo')),
            ],
            options={
                'verbose_name': 'pólo',
                'verbose_name_plural': 'pólos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('codigo', models.CharField(max_length=255, unique=True, verbose_name='código da turma')),
                ('periodo_ano', models.CharField(max_length=255, verbose_name='período de oferta (ano)')),
                ('periodo_mes', models.CharField(max_length=255, verbose_name='período de oferta (mês)')),
                ('periodo_curso', models.CharField(max_length=255, verbose_name='período do curso')),
                ('turno', models.IntegerField(choices=[(1, 'Noturno'), (2, 'Vespertino'), (3, 'Matutino'), (5, 'EAD'), (6, 'Diurno'), (7, 'Integral')], max_length=255, verbose_name='turno')),
                ('active', models.BooleanField(verbose_name='ativo?')),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avaportal.campus')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avaportal.curso')),
            ],
            options={
                'verbose_name': 'turma',
                'verbose_name_plural': 'turmas',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='quando ocorreu')),
                ('requisicao', models.TextField(blank=True, null=True, verbose_name='requisição')),
                ('requisicao_header', models.TextField(blank=True, null=True, verbose_name='cabeçalho da requisição')),
                ('requisicao_invalida', models.TextField(blank=True, null=True, verbose_name='requisição inválida')),
                ('resposta', models.TextField(blank=True, null=True, verbose_name='resposta')),
                ('resposta_header', models.TextField(blank=True, null=True, verbose_name='cabeçalho da resposta')),
                ('resposta_invalida', models.TextField(blank=True, null=True, verbose_name='resposta inválida')),
                ('status', models.CharField(blank=True, choices=[('S', 'Noturno'), ('F', 'Vespertino')], max_length=255, null=True, verbose_name='status')),
                ('status_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='status code')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='avaportal.campus')),
            ],
            options={
                'verbose_name': 'Solicitação',
                'verbose_name_plural': 'Solicitações',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suap_id', models.CharField(max_length=255, unique=True, verbose_name='ID no SUAP')),
                ('codigo', models.CharField(max_length=255, unique=True, verbose_name='código do diário')),
                ('situacao', models.CharField(max_length=255, verbose_name='situação')),
                ('descricao', models.CharField(max_length=255, verbose_name='descrição')),
                ('descricao_historico', models.CharField(max_length=255, verbose_name='descrição no histórico')),
                ('sigla', models.CharField(max_length=255, verbose_name='sigla')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avaportal.turma')),
            ],
            options={
                'verbose_name': 'diário',
                'verbose_name_plural': 'diários',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='usuário')),
                ('nome', models.CharField(max_length=255, verbose_name='nome do usuário')),
                ('email', models.CharField(max_length=255, verbose_name='e-Mail principal')),
                ('email_institucional', models.CharField(max_length=255, verbose_name='e-Mail institucional')),
                ('email_escolar', models.CharField(max_length=255, verbose_name='e-Mail escolar')),
                ('email_academico', models.CharField(max_length=255, verbose_name='e-Mail academico')),
                ('email_pessoal', models.CharField(max_length=255, verbose_name='e-Mail pessoal')),
                ('tipo', models.CharField(max_length=255, verbose_name='tipo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='equipe')),
                ('is_active', models.BooleanField(default=True, verbose_name='ativo')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superusuário')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de registro')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='último login')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='avaportal.campus', verbose_name='Campus')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='grupos')),
                ('polo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='avaportal.polo', verbose_name='Pólo')),
            ],
            options={
                'verbose_name': 'usuário',
                'verbose_name_plural': 'usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
