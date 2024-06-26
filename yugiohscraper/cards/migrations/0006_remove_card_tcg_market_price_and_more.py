# Generated by Django 5.0.3 on 2024-04-18 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_alter_card_tcg_min_listing_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='tcg_market_price',
        ),
        migrations.RemoveField(
            model_name='card',
            name='tcg_min_listing',
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('tcg_market_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tcg_min_listing', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
    ]
