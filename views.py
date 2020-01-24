# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from .models import *
# from .forms import NewClimbForm
import datetime


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required(login_url='login/')
def view_climber(request):
    if not request.user.is_authenticated():
        raise Http404()

    view_climber_pk = request.GET.get('pk', None)
    if view_climber_pk is not None:
        climber = Climber.objects.filter(pk=view_climber_pk)
        if climber:
            context = collect_climber_info(climber)
        else:
            context =  None # what to do here?    
    else:
        context = None # what to do here?
    
    return render(request, 'cascade_mountain_climber/view_climber.html', context)

@login_required(login_url='login/')
def index(request):
    if not request.user.is_authenticated():
        raise Http404()

    climber, created = Climber.objects.get_or_create(user=request.user)
    climb_pk = request.GET.get('pk', None)

    if climb_pk is not None:
        request = delete(request, climb_pk)
        return redirect('/cascade_mountain_climber/')

    elif request.method == 'POST':
        register_new_climb(request, climber)

    #  get user climber stats
    context = collect_climber_info(climber)
   
    return render(request, 'cascade_mountain_climber/index.html', context)

def collect_climber_info(climber):
    climbs = Climb.objects.filter(climber=climber)
    climbed_mtns = []
    for climb in climbs:
        climbed_mtns.append(climb.mountain)

    # mountains = Mountain.objects.values_list('name', flat=True)
    mountains = Mountain.objects.all()

    # get leaderboard stats
    superuser = User.objects.get(username="master")
    all_climbers = Climber.objects.exclude(user=superuser)
    leaderboard = []
    for lb_climber in all_climbers:
        leaderboard.append({
            'name': lb_climber.user.username,
            'total_climbs': lb_climber.get_total_climbs(),
            'unique_climbs': lb_climber.get_unique_climbs()
        })

    context = {
        'climbs': climbs,
        'mountains': mountains,
        'climbed_mtns': climbed_mtns,
        'climber_name': climber.user.username,
        'total_climbs': climber.get_total_climbs(),
        'unique_climbs': climber.get_unique_climbs(),
        'lb_stats': leaderboard,
        # 'form': form
    }
    return context

def delete(request, climb_pk):
    climb = Climb.objects.filter(pk=climb_pk).first()
    if climb:
        climb.delete()
        print 'deleted climb: ', climb
    else:
        print 'ERROR: Climb pk {0} not found'.format(climb_pk)
    return request

def register_new_climb(request, climber):
    mountain_name = request.POST.get('mountain', None)
    route = request.POST.get('route', None)
    date = request.POST.get('date', None)
    print 'date: ', date

    if not mountain_name or mountain_name == "Select a Mountain":
        print 'none in values'

    else:
        print "climb info: ", mountain_name, route, date
        if date:
            # date = date.split()[0] # remove time
            date = datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
        mountain = Mountain.objects.get(name=mountain_name)

        climb = Climb.objects.filter(climber=climber,
                                     mountain=mountain,
                                     date_climbed=date,
                                     route_climbed=route)
        if not climb:
            climb = Climb.objects.create(climber=climber,
                                         mountain=mountain,
                                         date_climbed=date,
                                         route_climbed=route
                                        )
            climber.add_climb_to_total(climb)
        else:
            print 'climb already exists'

        print mountain_name, route, date, climber.total_climbs

    # form = NewClimbForm(request.POST)
    # if form.is_valid():
    #     print 'registering new climb'
    # else:
    #     form = NewClimbForm()
    #     print 'not a post, get blank form'
