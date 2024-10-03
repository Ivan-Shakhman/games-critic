# Generated by Django 5.1.1 on 2024-09-23 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesAndReviews', '0004_alter_game_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['username'], 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AddField(
            model_name='author',
            name='favorite_games',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite_by', to='gamesAndReviews.game'),
        ),
    ]
