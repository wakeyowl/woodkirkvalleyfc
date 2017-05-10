from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, render_to_response, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.generic import ListView
from registration.backends.simple.views import RegistrationView
from django.views.generic.edit import UpdateView

from member.forms import UserMemberForm, UserMemberAddChildForm, UserMemberUpdateView
from member.models import UserMember, Player


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

    current_user = UserMember.objects.filter(user_id=user)
    player_list = Player.objects.filter(member_parent_id=user).prefetch_related('manager__player_set')
    player_list.order_by('manager__full_name')
    # address_list = UserMember.objects.filter(member_parent_id=user)
    context_dict = {'player': player_list, 'loggedin_user': current_user}

    # userprofile = User.objects.get(username=user)
    # form = UserMemberAddChildForm({})

    return render(request, 'member/profile.html', context=context_dict)


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
                page.member_parent_id = user
                page.save()

                return profile(request)

        else:
            print(form.errors)

    context_dict = {'form': form, 'member_parent_id': user}

    return render(request, 'member/add_player.html', context_dict)


@login_required
def edit_usermember(request):
    try:
        id = request.user.pk
    except  User.DoesNotExist:
        return redirect('index')

    instance = get_object_or_404(UserMember, user=id)
    form = UserMemberUpdateView()

    if request.method == 'POST':
        form = UserMemberUpdateView(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()

            return profile(request)
    else:
        context_dict = {'form': form}
    return render(request, 'member/usermember_update_form.html', context_dict)
