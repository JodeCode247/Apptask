# Generated by Django 5.0.7 on 2024-12-25 04:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminApps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('points_reward', models.CharField(max_length=255, null=True)),
                ('app_icon', models.ImageField(upload_to='app_icons/')),
                ('app_store_link', models.URLField()),
                ('category', models.CharField(choices=[('SOCIAL', 'Social'), ('SPORTS', 'Sports'), ('ENTERTAINMENT', 'Entertainment'), ('EDUCATION', 'Education'), ('EXCERCISE', 'Exercise')], max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='myusers',
            name='name',
        ),
        migrations.AddField(
            model_name='myusers',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='UserAppDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(null=True, upload_to='')),
                ('task_completed', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('download_date', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mytask.adminapps')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(null=True)),
                ('number_of_task_completed', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
