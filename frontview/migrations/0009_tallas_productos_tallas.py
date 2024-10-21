# Generated by Django 4.2.15 on 2024-09-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontview', '0008_alter_productos_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tallas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Extra Extra Large')], max_length=3, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='productos',
            name='tallas',
            field=models.ManyToManyField(to='frontview.tallas'),
        ),
    ]