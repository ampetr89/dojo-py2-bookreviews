# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_user_pw_salt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('content', models.TextField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.User')),
            ],
        ),
    ]
