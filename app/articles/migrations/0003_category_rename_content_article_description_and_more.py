# Generated by Django 4.1.5 on 2023-01-06 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_author_alter_article_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name="article",
            old_name="content",
            new_name="description",
        ),
        migrations.AddField(
            model_name="article",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="files"),
        ),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="articles.category",
            ),
            preserve_default=False,
        ),
    ]