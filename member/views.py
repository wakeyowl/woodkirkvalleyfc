import email
from datetime import datetime

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import *
from django.contrib import messages
from registration.backends.simple.views import RegistrationView

from member.forms import UserMemberForm, UserMemberAddChildForm, UserMemberUpdateForm, AccidentForm, \
    UserMemberUpdatePlayerForm, PasswordResetRequestForm

from member.models import UserMember, Player, TeamManagers
from woodkirkvalleydata.settings import DEFAULT_FROM_EMAIL


class ResetPasswordRequestView(FormView):
    # code for template is given below the view's code
    template_name = "account/test_template.html"
    success_url = '/admin/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'registration/password_reset_subject.txt'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_subject.txt
        # to templates directory
        email_template_name = 'registration/password_reset_email.html'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_email.html
        # to templates directory
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data["email_or_username"]
            # uses the method written above
            if self.validate_email_address(data) is True:
                '''
                If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(
                    Q(email=data) | Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        self.reset_password(user, request)

                    result = self.form_valid(form)
                    messages.success(request,
                                     'An email has been sent to {0}. Please check its inbox to continue reseting '
                                     'password.'.format(
                                         data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'No user is associated with this email address')
                return result
            else:
                '''
                If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        self.reset_password(user, request)
                    result = self.form_valid(form)
                    messages.success(
                        request,
                        "Email has been sent to {0}'s email address. Please check its inbox to continue reseting "
                        "password.".format(
                            data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'This username does not exist in the system.')
                return result
            messages.error(request, 'Invalid Input')
        except Exception as e:
            print(e)
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "account/test_template.html"
    success_url = '/admin/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)

class WoodkirkRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


def update_user(request):
    userupdated = get_object_or_404(UserMember, user=request.user.pk)
    if request.method == "POST":
        form = UserMemberUpdateForm(request.POST, instance=userupdated)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('profile', )
    else:
        form = UserMemberUpdateForm(instance=userupdated)

    return render(request, 'member/usermember_update_form.html', {'form': form})


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    # last_visit_time = datetime.now()
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits


def register_accident(request):
    form = AccidentForm()
    if request.method == 'POST':
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)
    context_dict = {'form': form}

    return render(request, 'member/accident_form.html', context_dict)


@login_required
def register_profile(request):
    form = UserMemberForm()
    if request.method == 'POST':
        form = UserMemberForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('profile')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'member/profile_registration.html', context_dict)


def index(request):
    try:
        user = request.user.pk
    except User.DoesNotExist:
        return redirect('index')
    current_user = UserMember.objects.filter(user_id=user)
    context_dict = {'loggedin_user': current_user}
    response = render(request, 'member/index.html', context_dict)
    return response


def add_member(request):
    form = UserMemberForm()

    if request.method == 'POST':
        form = UserMemberForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)

    return render(request, 'member/add_member.html', {'form': form})


@login_required
def profile(request):
    try:
        user = request.user.pk
    except User.DoesNotExist:
        return redirect('index')
    try:
        current_user = UserMember.objects.filter(user_id=user)
        player_list = Player.objects.filter(member_parent_id=current_user[0].id).prefetch_related(
            'manager__player_set')
        player_list.order_by('manager__full_name')
        context_dict = {'player': player_list, 'loggedin_user': current_user}
        return render(request, 'member/profile.html', context=context_dict)
    except IndexError:
        # Handle users not completing the form properly
        return register_profile(request)


@login_required
def manager_profile(request):
    try:
        user = request.user.pk
    except User.DoesNotExist:
        return redirect('index')
    try:
        username = request.user.usermember.full_name
        managerlist = TeamManagers.objects.filter(full_name__istartswith=username)
        current_user = UserMember.objects.filter(user_id=user)
        player_list = Player.objects.filter(manager_id=managerlist).prefetch_related(
            'manager__player_set')
        player_list.order_by('name')
        context_dict = {'player': player_list, 'loggedin_user': current_user}
        return render(request, 'member/manager_profile.html', context=context_dict)
    except IndexError:
        return render(request, 'member/manager_profile.html', )


@login_required
def committee_profile(request):
    if request.user.is_superuser:
        try:
            player_list = Player.objects.filter().prefetch_related(
                'manager__player_set', 'member_parent__user')
            player_list = player_list.order_by('manager__full_name')
            context_dict = {'player': player_list, }
            return render(request, 'member/committee_profile.html', context=context_dict)

        except IndexError:
            return render(request, 'member/committee_profile.html', )
    else:
        return render(request, 'member/profile.html', )


@login_required
def addplayer(request):
    try:
        user = request.user.pk
    except User.DoesNotExist:
        return redirect('index')

    form = UserMemberAddChildForm()

    if request.method == 'POST':
        form = UserMemberAddChildForm(request.POST)
        if form.is_valid():
            if user:
                page = form.save(commit=False)
                current_user = UserMember.objects.filter(user_id=user)
                page.member_parent_id = current_user[0].id
                page.save()

                return profile(request)

        else:
            print(form.errors)

    context_dict = {'form': form, 'member_parent_id': user}

    return render(request, 'member/add_player.html', context_dict)


def update_player(request, player):
    player_updated = Player.objects.get_or_create(id=player)[0]
    form = UserMemberUpdatePlayerForm(instance=player_updated, )
    user = request.user.pk

    if request.method == 'POST':
        form = UserMemberUpdatePlayerForm(request.POST, request.FILES, instance=player_updated)

        if form.is_valid():
            # Check existing picture for clear
            try:
                if form.data['picture'] == '':
                    page = form.save(commit=False)
                    page.picture = form.data['picture']
                    page.save()
                    return profile(request)
                else:
                    form.save()
            except:
                # PIL Setup - Open and Resize
                picture_to_change = Image.open(form.instance.picture)
                picture_to_change = picture_to_change.resize((125, 125), Image.ANTIALIAS)

                # Get MetaData for the Save
                orig_picture_name = form.instance.name
                team = form.instance.manager.team
                team = team.replace(" ", "_")
                orig_picture_name = orig_picture_name.replace(" ", "_")

                # Save the new Image to disk
                picture_to_change.save("member/media/profile_images/" + team + "_" + orig_picture_name + ".jpg",
                                       quality=90)
                page = form.save(commit=False)

                # Call to override save function in Player Model
                page.save()

                return profile(request)
        else:
            print(form.errors)
    else:

        return render(request, 'member/userplayer_update_form.html', {'form': form})
    return render(request, 'member/userplayer_update_form.html', {'form': form})
