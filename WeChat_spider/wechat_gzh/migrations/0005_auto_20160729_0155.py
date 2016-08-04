# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_gzh', '0004_auto_20160728_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('publish_date', models.DateField()),
                ('source_url', models.URLField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GZH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('weixin_id', models.CharField(max_length=50, unique=True)),
                ('qr_code', models.URLField()),
                ('introduction', models.CharField(max_length=500)),
                ('verify_name', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='gzh_info',
            name='gzh_name',
        ),
        migrations.RemoveField(
            model_name='gzh_paper_list',
            name='gzh_name',
        ),
        migrations.DeleteModel(
            name='GZH_info',
        ),
        migrations.DeleteModel(
            name='GZH_list',
        ),
        migrations.DeleteModel(
            name='GZH_paper_list',
        ),
        migrations.AddField(
            model_name='article',
            name='gzh',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat_gzh.GZH'),
        ),
    ]
