# Generated by Django 4.0.3 on 2022-03-15 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='due_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='start_date',
            field=models.DateField(),
        ),
    ]
