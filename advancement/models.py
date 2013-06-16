from django.contrib.auth.models import User
from django.db import models

class Scout(models.Model):
	# user = models.OneToOneField(User, unique=True)
	# birth_date = models.DateField(blank=True, null=True)
	patrol = models.CharField(max_length=50, blank=True, null=True)
	rank = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True, null=True)

class Parent(models.Model):
	user = models.OneToOneField(User, unique=True)
	scouts = models.ManyToManyField(Scout, blank=True, null=True)

class Rank(models.Model):
	weight = models.IntegerField()
	name = models.CharField(max_length=30)
	number_required_meritbadges = models.IntegerField()
	number_optional_meritbadges = models.IntegerField()

class ScoutRank(models.Model):
	scout = models.ForeignKey(Scout)
	rank = models.ForeignKey(Rank)
	date_earned = models.DateField(blank=True, null=True)
	date_awarded = models.DateField(blank=True, null=True)

class MeritBadge(models.Model):
	name = models.CharField(max_length=100)
	required = models.BooleanField()
	alternates = models.CharField(max_length=200)

class ScoutMeritBadge(models.Model):
	scout = models.ForeignKey(Scout)
	merit_badge = models.ForeignKey(MeritBadge)
	goal_date = models.DateField(blank=True, null=True)
	date_earned = models.DateField(blank=True, null=True)
	date_awarded = models.DateField(blank=True, null=True)

class MeritBadgeBook(models.Model):
	merit_badge = models.ForeignKey(MeritBadge)
	owner = models.CharField(max_length=70)
	quantity = models.IntegerField()

class ScoutMeritBadgeBook(models.Model):
	scout = models.ForeignKey(Scout)
	merit_badge_book = models.ForeignKey(MeritBadgeBook)
	date_requested = models.DateField(blank=True, null=True)
	date_borrowed = models.DateField(blank=True, null=True)
	date_due = models.DateField(blank=True, null=True)
	date_returned = models.DateField(blank=True, null=True)

class MeritBadgeCounselor(models.Model):
	user = models.OneToOneField(User, unique=True)
	merit_badge = models.ForeignKey(MeritBadge)
	date_requested = models.DateField(blank=True, null=True)
	date_started = models.DateField(blank=True, null=True)
	registered = models.BooleanField()
	active = models.BooleanField()