# Generated by Django 4.0.4 on 2022-05-19 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0011_customer_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, default='preson.png', null=True, upload_to=''),
        ),
    ]