# Generated by Django 3.1.4 on 2020-12-20 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201220_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Image URL'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Starting Bid Amount'),
        ),
    ]
