# Generated by Django 3.1.4 on 2020-12-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
