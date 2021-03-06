# Generated by Django 2.1.3 on 2018-11-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.PositiveIntegerField(verbose_name='Column')),
                ('row', models.PositiveIntegerField(verbose_name='Row')),
                ('column_span', models.PositiveIntegerField(verbose_name='Column span')),
                ('row_span', models.PositiveIntegerField(verbose_name='Row span')),
                ('advanced', models.CharField(max_length=3, verbose_name='Advanced')),
                ('font_size', models.PositiveSmallIntegerField(verbose_name='Font size')),
                ('direction', models.BooleanField(verbose_name='Direction')),
                ('vertical_align', models.CharField(blank=True, choices=[('t', 'Top'), ('m', 'Middle'), ('b', 'Bottom')], default='m', max_length=1, verbose_name='Vertical align')),
                ('horizontal_align', models.CharField(blank=True, choices=[('l', 'Left'), ('c', 'Center'), ('r', 'Right')], default='h', max_length=1, verbose_name='Horizontal align')),
                ('width', models.PositiveIntegerField(verbose_name='Width')),
                ('height', models.PositiveIntegerField(verbose_name='Height')),
                ('value', models.CharField(max_length=500, verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_in_load', models.PositiveIntegerField(verbose_name='Column in load')),
                ('column_in_plan', models.PositiveIntegerField(verbose_name='Column in plan')),
                ('name_in_load', models.CharField(max_length=100, verbose_name='Name in load')),
                ('name_in_plan', models.CharField(max_length=100, verbose_name='Name in plan')),
                ('font_size', models.PositiveSmallIntegerField(verbose_name='Font size')),
                ('advanced', models.CharField(max_length=3, verbose_name='Advanced')),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ScienceDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ScienceTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
