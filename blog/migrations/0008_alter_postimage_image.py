# Generated by Django 4.1.4 on 2022-12-27 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_allow_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(upload_to='articles/content/'),
        ),
    ]
