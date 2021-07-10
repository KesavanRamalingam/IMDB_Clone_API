# Generated by Django 3.2.4 on 2021-06-13 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchmate_app', '0002_auto_20210613_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='watchmate_app.streamplatform'),
            preserve_default=False,
        ),
    ]
