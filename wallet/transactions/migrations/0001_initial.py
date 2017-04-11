# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 23:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2017, 4, 10, 23, 4, 10, 919429))),
                ('current', models.BooleanField(default=False)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Wallet')),
            ],
            options={
                'verbose_name': 'PayPeriod',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('trans_type', models.IntegerField(choices=[(0, 'Income'), (1, 'Expense')])),
                ('frequency', models.IntegerField(choices=[(0, 'BiWeekly'), (1, 'Monthly')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('completed', models.BooleanField(default=False)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Wallet')),
            ],
        ),
        migrations.AddField(
            model_name='occurrence',
            name='payperiod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.PayPeriod'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Transaction'),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('wallet', 'name')]),
        ),
    ]
