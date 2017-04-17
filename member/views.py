from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from registration.backends.simple.views import RegistrationView
from django.views.generic.edit import UpdateView

from member.forms import UserMemberForm, UserMemberAddChildForm
from member.models import UserMember, Player, Contact, Badges, BadgeAssesments


class WoodkirkRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


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


@login_required
def register_profile(request):
    form = UserMemberForm()
    if request.method == 'POST':
        form = UserMemberForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'member/profile_registration.html', context_dict)


def index(request):
    response = render(request, 'member/index.html', {})
    return response


def merit_badges(request):
    meritbadge_list = Badges.objects.filter(levels='M')
    badgeassessment_list = BadgeAssesments.objects.all()
    context_dict = {'merit': meritbadge_list, 'meritassessments': badgeassessment_list}
    response = render(request, 'member/merit_badges.html', context=context_dict)
    return response


def skills_matrix(request):
    response = render(request, 'member/skills_matrix.html', {})
    return response


def attacking(request):
    response = render(request, 'member/skills/attacking.html', {})
    return response


def kickups(request):
    response = render(request, 'member/skills/kickups.html', {})
    return response


def defending(request):
    response = render(request, 'member/skills/defending.html', {})
    return response


def teamwork(request):
    response = render(request, 'member/skills/teamwork.html', {})
    return response


def leadership(request):
    response = render(request, 'member/skills/leadership.html', {})
    return response


def technical(request):
    response = render(request, 'member/technical.html', {})
    return response


def social(request):
    response = render(request, 'member/social.html', {})
    return response


def physical(request):
    response = render(request, 'member/physical.html', {})
    return response


def psychological(request):
    response = render(request, 'member/psychological.html', {})
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


class UserMemberUpdate(UpdateView):
    model = UserMember
    form_class = UserMemberForm
    fields = ['address1', 'address2', 'city', 'postcode', 'mobile_phone']
    template_name = 'member/usermember_update_form.html'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        return user.userprofile

    def get_success_url(self, *args, **kwargs):
        return reverse("index.html")

        # def __init__(self):
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return redirect('index')

        # if request.method == 'POST':
        #     form = UserMemberForm(request.POST)
        #     form.user = User.objects.get(username=username)
        #     if form.is_valid():
        #         user_profile = form.save(commit=False)
        #         user_profile.user = request.user
        #         user_profile.save()
        #
        #         return index(request)
        #     else:
        #         print(form.errors)
        #
        # return render(request, 'member/usermember_update_form.html', {'form': form})


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    player_list = Player.objects.filter(member_parent__username=user)
    address_list = UserMember.objects.filter(member_parent__username=user)
    context_dict = {'player': player_list, 'address': address_list}

    userprofile = User.objects.get(username=username)
    form = UserMemberAddChildForm({})

    return render(request, 'member/profile.html', context=context_dict)


@login_required
def add_player(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    form = UserMemberAddChildForm()

    if request.method == 'POST':
        form = UserMemberAddChildForm(request.POST)
        if form.is_valid():
            if user:
                page = form.save(commit=False)
                page.member_parent = user
                page.save()

                return profile(request, username)

        else:
            print(form.errors)

    context_dict = {'form': form, 'member_parent_id': user}

    return render(request, 'member/add_player.html', context_dict)


class ListContactView(ListView):
    model = Contact
    template_name = 'contact_list.html'
