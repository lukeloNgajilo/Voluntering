# Generated by Django 3.0.1 on 2020-08-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvs', '0005_push'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='subjects',
            field=models.CharField(choices=[('Arts', 'Arts'), ('Science', 'Science')], default='Arts', max_length=10),
            preserve_default=False,
        ),
    ]
