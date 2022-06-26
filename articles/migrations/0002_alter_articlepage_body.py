# Generated by Django 4.0.5 on 2022-06-26 22:14

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.fields.StreamField([('paragraph', wagtail.blocks.RichTextBlock()), ('embed', wagtail.blocks.RawHTMLBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=None),
        ),
    ]