from django.db import models
from django.template.defaultfilters import slugify
from django.forms import extras, forms


class Member(models.Model):
    name = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=12)
    email = models.EmailField()
    phone = models.IntegerField()
    slug = models.SlugField(unique=True)
    consent = models.BooleanField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=128)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1)
    member_parent = models.ForeignKey(Member)
    medical_details = models.TextField()

    def __str__(self):
        return self.name