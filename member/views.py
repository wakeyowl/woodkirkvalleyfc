import os
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

from member.forms import UserMemberForm, UserMemberAddChildForm, UserMemberUpdateForm, AccidentForm, \
    UserMemberUpdatePlayerForm
from member.models import UserMember, Player


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
    try:
        current_user = UserMember.objects.filter(user_id=user)
        player_list = Player.objects.filter(member_parent_id=current_user[0].id).prefetch_related(
            'manager__player_set')
        player_list.order_by('manager__full_name')
        context_dict = {'player': player_list, 'loggedin_user': current_user}
        return render(request, 'member/profile.html', context=context_dict)
    except IndexError:
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
                if form.data['picture'] != '':
                    page = form.save(commit=False)
                    page.save()
                else:
                    form.save()
                    return profile(request)
            except:
                page = form.save(commit=False)
                page.save()

                return profile(request)
        else:
            print(form.errors)
    else:

        return render(request, 'member/userplayer_update_form.html', {'form': form})
    return render(request, 'member/userplayer_update_form.html', {'form': form})