from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from resizeimage import resizeimage
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TeamManagers(models.Model):
    full_name = models.CharField(max_length=128, unique=True, null=True)
    team = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.CharField(max_length=100, null=True)
    CLUB_ROLE = (
        ('MANAGER', 'Manager'),
        ('COACH', 'Coach'),
        ('COMMITTEE', 'Committee'),
    )

    def __str__(self):
        return ' '.join([
            self.full_name,
            self.team,
        ])

    class Meta:
        verbose_name_plural = "Managers"


@python_2_unicode_compatible
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
    accepted_code_of_conduct = models.NullBooleanField(choices=CONSENT_CHOICES,
                                                       max_length=3,
                                                       blank=True, null=True, default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(UserMember, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "User Members"


@python_2_unicode_compatible
class Player(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    manager = models.ForeignKey(TeamManagers, on_delete=models.CASCADE, blank=False)
    birthdate = models.DateField()
    member_parent = models.ForeignKey(UserMember, on_delete=models.CASCADE, blank=False)
    medical_details = models.TextField()
    picture = models.ImageField(upload_to='profile_images/', blank=True)
    is_active = models.BooleanField(default=False)
    CONSENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    accepted_code_of_conduct = models.NullBooleanField(choices=CONSENT_CHOICES,
                                                       max_length=3,
                                                       blank=True, null=True, default=True)

    class Meta:
        unique_together = ('birthdate', 'name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            pil_image_obj = Image.open(self.picture)
            new_image = resizeimage.resize_width(pil_image_obj, 150)

            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            # Get MetaData for the Save
            orig_picture_name = self.name
            orig_picture_name = orig_picture_name.replace(" ", "_")
            team = self.manager.team
            team = team.replace(" ", "_")

            temp_name = '' + team + '_' + orig_picture_name + '.jpg'
            self.picture.delete(save=False)

            self.picture.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        except:
            #temp_name = None
            # Handle Null Setting of Image (Clear Route)
            super(Player, self).save()
        # if temp_name is None:
        #     super(Player, self).save()
        #     #super(Player, self).clean(*args, **kwargs)
        # else:

        # If Not save the in memory image to disk ans set it to db
        super(Player, self).save(*args, **kwargs)


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

    class Meta:
        verbose_name_plural = "Membership Types"


class Seasons(models.Model):
    description = models.CharField(max_length=200)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    class Meta:
        verbose_name_plural = "Seasons"


class Payments(models.Model):
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=200)
    date_taken = models.DateField()
    player = models.ForeignKey('Player', on_delete=models.CASCADE, )
    manager = models.ForeignKey('TeamManagers', on_delete=models.CASCADE, )
    PLAYER_MEMBERSHIP = 'Player Membership'
    CLUB_MEMBERSHIP = 'Club Membership'
    DONATION = 'Club Donation'
    PAYMENT_TYPES = (
        (PLAYER_MEMBERSHIP, 'Player Membership'),
        (CLUB_MEMBERSHIP, 'Club Membership'),
        (DONATION, 'Club Donation'),
    )
    paymentType = models.CharField(max_length=20, choices=PAYMENT_TYPES)

    class Meta:
        verbose_name_plural = "Payments"


class Accident(models.Model):
    # Section 1
    ACC_TYPES = (
        ('ACCIDENT', 'Accident'),
        ('DANGEROUS OCCURANCE', 'Dangerous Occurance'),
        ('WORK RELATED', 'Work Related'),
        ('NEAR MISS', 'Near Miss'),
    )
    accident_type = models.CharField(max_length=200, choices=ACC_TYPES)
    person_injured = models.CharField(max_length=200)
    person_injured_address = models.CharField(max_length=200, null=True)
    person_injured_postcode = models.CharField(max_length=12, null=True)
    person_injured_mobile_phone = models.CharField(max_length=12, null=True, blank=True)

    accident_date = models.DateTimeField()
    # Section 2
    accident_location = models.CharField(max_length=200, null=True, help_text='Where did it happen?')
    accident_reason = models.CharField(max_length=200, null=True, help_text='How did it happen?')
    injury_sustained = models.CharField(max_length=200, null=True, help_text='Give details of the injury?')
    # Section 3
    FIRST_AID_OUTCOME = (
        ('ACCEPTED', 'Accepted'),
        ('REFUSED', 'Refused'),
        ('HOSPITAL', 'Hospital'),
    )
    first_aid_outcome = models.CharField(max_length=200, choices=FIRST_AID_OUTCOME)
    first_aid_given = models.CharField(max_length=200, help_text='What first aid was given?')
    first_aid_person = models.CharField(max_length=100, help_text='Who gave the first aid?')
    first_aid_hospitalised = models.BooleanField(help_text='Did the injured person need to attend hospital?')
    hospital_more_than_24 = models.BooleanField(help_text='Was the injured person in hospital for more than 24 hours?')
    hospital_name = models.CharField(max_length=200, help_text='Which hospital did they visit?')
