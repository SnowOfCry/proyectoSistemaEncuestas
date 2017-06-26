# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-20 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreEncuesta', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=255)),
                ('visitas', models.IntegerField(default=0)),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestaapp.Encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('votosRespuesta', models.IntegerField(default=0)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestaapp.Pregunta')),
            ],
        ),
    ]
