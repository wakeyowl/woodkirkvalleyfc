from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class TeamManagers(models.Model):
    full_name = models.CharField(max_length=128, unique=True, null=True)
    team = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class UserMember(models.Model):
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=128, unique=True, null=True)
    address1 = models.CharField(max_length=128, null=True)
    address2 = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    postcode = models.CharField(max_length=12, null=True)
    mobile_phone = models.CharField(max_length=12, null=True, blank=True)
    slug = models.SlugField(unique=True)
    CONSENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    consent = models.NullBooleanField(choices=CONSENT_CHOICES,
                                      max_length=3,
                                      blank=True, null=True, default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(UserMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Player(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    manager = models.ForeignKey(TeamManagers, on_delete=models.CASCADE)
    birthdate = models.DateField()
    member_parent = models.ForeignKey(User)
    medical_details = models.TextField()

    class Meta:
        unique_together = ('birthdate', 'name',)

    def __str__(self):
        return self.name


class MembershipType(models.Model):
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    season = models.ForeignKey('Seasons', on_delete=models.CASCADE, )
    PLAYER = 'PLAYER'
    CLUB = 'CLUB'
    MEMBER_TYPES = (
        (PLAYER, 'Player'),
        (CLUB, 'Club'),
    )
    type = models.CharField(max_length=6, choices=MEMBER_TYPES)


class Seasons(models.Model):
    description = models.CharField(max_length=200)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
