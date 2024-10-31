# Generated by Django 5.1.2 on 2024-10-31 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TabelaUsuarios",
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
                ("nome_usuario", models.CharField(max_length=40)),
                ("email", models.EmailField(max_length=254)),
                ("senha", models.CharField(max_length=64)),
            ],
            options={"verbose_name": "Tabela_Usuario",},
        ),
    ]