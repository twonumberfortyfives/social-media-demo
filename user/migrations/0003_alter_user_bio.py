# Generated by Django 5.1.1 on 2024-09-19 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
