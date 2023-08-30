# Generated by Django 3.2.20 on 2023-08-04 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('publishedDate', models.DateField()),
                ('average_rating', models.IntegerField(blank=True, null=True)),
                ('ratings_count', models.IntegerField(blank=True, null=True)),
                ('thumbnail', models.URLField(blank=True, null=True)),
                ('authors', models.ManyToManyField(to='library.Author')),
                ('categories', models.ManyToManyField(blank=True, to='library.Category')),
            ],
        ),
    ]