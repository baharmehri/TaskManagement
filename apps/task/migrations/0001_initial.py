# Generated by Django 4.2.14 on 2024-09-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('pending', 'Pending'), ('completed),', 'Completed'), ('done', 'Done'), ('failed', 'Failed')], default='pending', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
