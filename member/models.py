from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserMember(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=128, unique=True)
    address_street = models.CharField(max_length=128)
    address_town_city = models.CharField(max_length=128)
    postcode = models.CharField(max_length=12)
    phone = models.IntegerField()
    slug = models.SlugField(unique=True)
    consent = models.BooleanField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(UserMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=128)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1)
    member_parent = models.ForeignKey(UserMember)
    medical_details = models.TextField()

    class Meta:
        unique_together = ('birth_date', 'name',)

    def __str__(self):
        return self.name