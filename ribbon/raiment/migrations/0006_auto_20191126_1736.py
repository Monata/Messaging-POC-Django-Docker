# Generated by Django 2.2.5 on 2019-11-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raiment', '0005_delete_clothing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='color_tag',
        ),
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
        migrations.AddField(
            model_name='item',
            name='colour',
            field=models.CharField(default='red', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='image_link',
            field=models.URLField(default='https://assets.pokemon.com/assets/cms2/img/pokedex/full/202.png'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='material',
            field=models.CharField(default='Cotton', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(default=399),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(default='Medium', max_length=8),
            preserve_default=False,
        ),
    ]