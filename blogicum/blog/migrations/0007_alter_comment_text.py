# Generated by Django 3.2.16 on 2023-06-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=512, verbose_name='Текст'),
        ),
    ]
