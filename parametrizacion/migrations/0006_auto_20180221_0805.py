# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-21 08:05
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametrizacion', '0005_auto_20171229_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='empresa',
            name='rut',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_rut', message='Rut no valido', regex='^([0-9]+-[0-9K])$')]),
        ),
        migrations.AlterField(
            model_name='persona',
            name='estadoCivil',
            field=models.CharField(choices=[('0', '[Seleccione...]'), ('S', 'Soltero'), ('C', 'Casado'), ('O', 'Otro')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='empresausuario',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametrizacion.Empresa'),
        ),
        migrations.AddField(
            model_name='empresausuario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='empresausuario',
            unique_together=set([('usuario', 'empresa')]),
        ),
    ]
