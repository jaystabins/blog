# Generated by Django 4.1.4 on 2022-12-18 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_post_image_post_tagline_alter_post_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default="../static/img/smokeymtn.jpg", upload_to="media/articles/"
            ),
        ),
    ]
