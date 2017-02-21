from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserMember(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=128, unique=True, null=True)
    address_street = models.CharField(max_length=128, null=True)
    address_town_city = models.CharField(max_length=128, null=True)
    postcode = models.CharField(max_length=12, null=True)
    phone = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    # consent = models.BooleanField()
    LOCATOR_YES_NO_CHOICES = ((None, ''), (True, 'Yes'), (False, 'No'))
    consent = models.NullBooleanField(choices=LOCATOR_YES_NO_CHOICES,
                                      max_length=3,
                                      blank=True, null=True, default=None, )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(UserMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.user


class Player(models.Model):
    name = models.CharField(max_length=128)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1)
    member_parent = models.ForeignKey(User)
    medical_details = models.TextField()

    class Meta:
        unique_together = ('birthdate', 'name',)

    def __str__(self):
        return self.name
