# Generated by Django 2.1.5 on 2020-06-03 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('davinci', '0003_user_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='login_count',
            field=models.PositiveIntegerField(null=True),
        ),
    ]