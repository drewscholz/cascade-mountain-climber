# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     pass

class Climber(models.Model):
    user = models.OneToOneField(User)
    total_climbs = models.IntegerField(default=0)
    unique_climbs = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s"%(self.user)

    def add_climb_to_total(self, climb):
        self.total_climbs += 1
        # we just created this climb so we expect this to match the climb argument
        just_made = Climb.objects.filter(climber=self, mountain=climb.mountain)
        if len(just_made) == 1 and just_made[0] == climb:
            self.unique_climbs += 1
        self.save()

    def get_total_climbs(self):
        return len(Climb.objects.filter(climber=self))

    def get_unique_climbs(self):
        return len(Climb.objects.filter(climber=self).values('mountain').distinct())


class Mountain(models.Model):
    name = models.CharField(max_length=20)
    elevation = models.IntegerField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    location = models.CharField(max_length=20, null=True)
    # climbers = models.ManyToManyField(Climber, through='Climb')

    def __unicode__(self):
        return "%s"%(self.name)


class Climb(models.Model):
    climber = models.ForeignKey(Climber, null=True)
    mountain = models.ForeignKey(Mountain, null=True)
    date_climbed = models.DateField()
    route_climbed = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return "%s - %s - %s - %s"%(self.climber, self.mountain,
        self.route_climbed, self.date_climbed)


# class Climb(models.Model):
#     mountain_name = models.CharField(max_length=20)
#     climbing_route = models.CharField(max_length=50)
#     climb_date = models.DateField()
#     climber = models.ManyToManyField(Climber)
#
#     def __unicode__(self):
#         return "%s - %s - %s"%(self.mountain_name, self.climbing_route, self.climb_date)
