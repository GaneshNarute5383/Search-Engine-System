from django.db import models


# Create your models here.
class WebContent(models.Model):
    webpage_url = models.CharField(max_length=300)
    webpage_title = models.CharField(max_length=500)
    webpage_description = models.TextField(max_length=999)
    webpage_keywords = models.TextField(max_length=1000)


class Keywords(models.Model):
    kname = models.CharField(max_length=100, unique=True)


class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)


class Feedback(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    feedback = models.TextField(max_length=1000)


class SitemapInfo(models.Model):
    url = models.CharField(max_length=100)
    sitemap = models.CharField(max_length=100)

class SignUp(models.Model):
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10)
    password = models.CharField(max_length=15)
    conformed_password = models.CharField(max_length=15)

