# Generated by Django 3.1.14 on 2023-05-31 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_featureflags'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignpage',
            name='cta_first',
            field=models.BooleanField(default=False, help_text='Check this to shift the CTA to the top on mobile'),
        ),
        migrations.AddField(
            model_name='campaignpage',
            name='intro_header',
            field=models.CharField(blank=True, default='Donate now', max_length=200),
        ),
    ]
