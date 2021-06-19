# Generated by Django 3.0.5 on 2020-05-07 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Userid', models.IntegerField()),
                ('Title', models.CharField(max_length=100)),
                ('Public', models.BooleanField()),
                ('Body', models.TextField(max_length=100000)),
                ('Location', models.CharField(max_length=100)),
                ('SDate', models.DateField()),
                ('EDate', models.DateField()),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Userid', models.IntegerField()),
                ('FollowUserid', models.IntegerField()),
                ('FollowDate', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'follow',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Articleid', models.IntegerField()),
                ('LikeUserid', models.IntegerField()),
            ],
            options={
                'db_table': 'liketest',
            },
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Articleid', models.IntegerField()),
                ('Remark', models.TextField(max_length=100000)),
                ('RemarkUserid', models.IntegerField()),
                ('RemarkDate', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'remark',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=30, unique=True)),
                ('PassWord', models.CharField(max_length=30)),
                ('SignDate', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
