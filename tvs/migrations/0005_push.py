# Generated by Django 3.0.1 on 2020-07-07 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0004_cancelledapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userKey', models.CharField(max_length=400, null=True)),
                ('appKey', models.CharField(max_length=400, null=True)),
                ('appId', models.CharField(max_length=400, null=True)),
            ],
        ),
    ]