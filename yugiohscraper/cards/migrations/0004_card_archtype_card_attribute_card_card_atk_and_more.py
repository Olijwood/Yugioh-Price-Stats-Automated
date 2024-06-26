# Generated by Django 5.0.3 on 2024-04-02 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_remove_cardimage_image_cardimage_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='archtype',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='attribute',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='card_atk',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='card_def',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='level',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='lore',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='simple_type',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
