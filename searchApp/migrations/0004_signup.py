# Generated by Django 3.2.6 on 2021-09-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchApp', '0003_sitemapinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('mname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=15)),
                ('conformed_password', models.CharField(max_length=15)),
            ],
        ),
    ]
