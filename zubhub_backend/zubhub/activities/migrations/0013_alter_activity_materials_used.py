# Generated by Django 3.2 on 2023-08-31 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_alter_activity_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='materials_used',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
