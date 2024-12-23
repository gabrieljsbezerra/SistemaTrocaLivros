# Generated by Django 5.1.2 on 2024-10-30 01:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TabelaLivros",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome_livro", models.CharField(max_length=100)),
                ("autor", models.CharField(max_length=50)),
                ("co_autor", models.CharField(blank=True, max_length=50, null=True)),
                ("editora", models.CharField(max_length=30)),
                ("cateoria", models.CharField(max_length=30)),
                ("data_cadastro", models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
