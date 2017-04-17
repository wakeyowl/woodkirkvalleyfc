from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


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
                                      blank=True, null=True, default=True )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(UserMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.user


class Player(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)

    birthdate = models.DateField()
    member_parent = models.ForeignKey(User)
    medical_details = models.TextField()

    class Meta:
        unique_together = ('birthdate', 'name',)

    def __str__(self):
        return self.name


class Contact(models.Model):

    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255, )
    email = models.EmailField()

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])


class Badges(models.Model):

    GOLD = 'G'
    SILVER = 'S'
    BRONZE = 'B'
    MERIT = 'M'
    BADGE_LEVELS = (
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BRONZE, 'Bronze'),
        (MERIT, 'Merit'),
    )
    TECHNICAL = 'TECH'
    PSYCHOLOGICAL = 'PSYCHOLOGICAL'
    PHYSICAL = 'PHYSICAL'
    SOCIAL = 'SOCIAL'
    BADGE_CATEGORIES = (
        (TECHNICAL, 'Technical'),
        (PSYCHOLOGICAL, 'Psychological'),
        (PHYSICAL, 'Physical'),
        (SOCIAL, 'Social'),
    )
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=255, choices=BADGE_CATEGORIES)
    levels = models.CharField(max_length=1, choices=BADGE_LEVELS)
    pageUrl = models.CharField(max_length=200)
    iconUrl = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BadgeAssesments(models.Model):

    badgeId = models.ForeignKey(Badges, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.description