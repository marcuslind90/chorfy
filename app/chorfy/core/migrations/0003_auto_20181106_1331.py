# Generated by Django 2.1.2 on 2018-11-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_article_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='keywords',
        ),
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword'),
        ),
    ]