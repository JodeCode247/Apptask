# Generated by Django 5.0.7 on 2024-12-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytask', '0003_alter_adminapps_app_icon_alter_adminapps_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='total_points',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
