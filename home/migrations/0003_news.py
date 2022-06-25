# Generated by Django 4.0.5 on 2022-06-25 17:37

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('body', wagtail.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'news',
                'ordering': ['-start_date'],
            },
        ),
    ]