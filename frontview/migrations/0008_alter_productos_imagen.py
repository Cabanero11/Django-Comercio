# Generated by Django 4.2.15 on 2024-09-06 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontview', '0007_alter_pedido_tefelono_alter_usuario_tefelono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(upload_to='productos/'),
        ),
    ]
