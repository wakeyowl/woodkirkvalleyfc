from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from bs4 import BeautifulSoup
import urllib2
import lxml
import re
from datetime import datetime
from timestring import Date
from json2html import *

from member.forms import UserMemberForm, UserMemberAddChildForm, UserMemberUpdateForm, AccidentForm, \
    UserMemberUpdatePlayerForm
from member.models import UserMember, Player, TeamManagers


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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', )
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


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


def get_fixtures(request):
    table_json = {}
    fixturesurls = {
        "url_garforth_boys": "http://full-time.thefa.com/ListPublicFixture.do?selectedFixtureGroupKey"
                             "=&selectedRelatedFixtureOption=2&selectedClub=655071567&selectedTeam"
                             "=&selectedFixtureDateStatus=&selectedFixtureStatus=&selectedDateCode=7days&selectednavpage1"
                             "=1&navPageNumber1=1&previousSelectedFixtureGroupKey=&previousSelectedClub=655071567"
                             "&seasonID=585273164&selectedSeason=585273164 "
    }

    def parseurl(url):
        index = 0
        global index
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read(), 'lxml')
        table = soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            if len(row.select('td')) > 0:
                cols = row.select('td')
                # Strip new lines and apostrophes
                table_json[index] = {"fixtureType": str(cols[0].text.strip('\n')),
                                     "date": str(cols[1].text.strip('\n')),
                                     "homeTeam": str(cols[2].text.strip('\n')).replace('\'', ''),
                                     "awayTeam": str(cols[3].text.strip('\n')).replace('\'', ''),
                                     "location": str(cols[4].text.strip('\n')).replace('\'', ''),
                                     "leagueDivision": str(cols[5].text.strip('\n'))}
                index = index + 1

    for key, url in fixturesurls.items():
        parseurl(url)

    home_games = {}
    count = 0
    for row in table_json:
        if table_json[row]['location'].startswith('Woodkirk Valley'):
            print
            table_json[row]
            home_games[count] = table_json[row]
            count += 1
    parsestring = str(home_games)
    parsestring = re.sub(r'[0-9]?[0-9]: {', "{", parsestring)
    parsestring = re.sub(r'(\d+)\'s', r'\1s', parsestring)
    parsestring = re.sub(r'\'', "\"", parsestring)
    parsestring = re.sub(r'^{', "{\"fixtures\": [ ", parsestring)
    parsestring = re.sub(r'}}$', "}]}", parsestring)
    outputtable = json2html.convert(json=parsestring)
    # Strip out the additional guff from json convertor
    outputtable = re.sub(r'<table border=\"1\"><th><tr>fixtures</th><td>', "", outputtable)
    # Bootstrap format the file
    outputtable = re.sub(r'<table border=\"1\">', "<table border=\"1\" class=\"table table-striped sorttable\">", outputtable)
    outputtable = re.sub(r'</table></td></tr></table>', "</table>", outputtable)
    # strip the outer table
    outputtable = re.sub(r'<table border="1" class="table table-striped sorttable"><tr><th>fixtures</th><td>', "", outputtable)
    context_dict = {'htmlfixtures': outputtable, 'jsonfixtures': parsestring}
    return render(request, 'member/fixtures.html', context_dict)


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
                page = form.save(commit=False)

                # Call to override save function in Player Model
                page.save()

                return profile(request)
        else:
            print(form.errors)
    else:

        return render(request, 'member/userplayer_update_form.html', {'form': form})
    return render(request, 'member/userplayer_update_form.html', {'form': form})
