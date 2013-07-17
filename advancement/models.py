from django.contrib.auth.models import User
from django.db import models

class Rank(models.Model):
	weight = models.IntegerField()
	name = models.CharField(max_length=30)
	number_required_meritbadges = models.IntegerField()
	number_optional_meritbadges = models.IntegerField()

	def __unicode__(self):
		return self.name

class Scouter(models.Model):
	user = models.OneToOneField(User, unique=True)
	birth_date = models.DateField(blank=True, null=True)
	role = models.CharField(max_length=50, blank=True, null=True) 
	patrol = models.CharField(max_length=50, blank=True, null=True)
	rank = models.ForeignKey(Rank, blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True, null=True)

	def __unicode__(self):
		return self.user.username

class Parent(Scouter):
	scouts = models.ManyToManyField(Scouter, blank=True, null=True, related_name='parent_scouts')

class ScoutRank(models.Model):
	scout = models.ForeignKey(Scouter)
	rank = models.ForeignKey(Rank)
	date_earned = models.DateField(blank=True, null=True)
	date_awarded = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return '{0} - {1}'.format(self.scout, self.rank)

class MeritBadge(models.Model):
	name = models.CharField(max_length=100)
	required = models.BooleanField()
	alternates = models.CharField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		return self.name

class ScoutMeritBadge(models.Model):
	scout = models.ForeignKey(Scouter)
	merit_badge = models.ForeignKey(MeritBadge)
	goal_date = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=255, blank=True, null=True)
	date_earned = models.DateField(blank=True, null=True)
	date_awarded = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return '{0} - {1}'.format(self.scout, self.merit_badge)

class MeritBadgeBook(models.Model):
	merit_badge = models.ForeignKey(MeritBadge)
	owner = models.CharField(max_length=70)
	quantity = models.IntegerField()

	def __unicode__(self):
		return self.merit_badge.name

class ScoutMeritBadgeBook(models.Model):
	scout = models.ForeignKey(Scouter)
	merit_badge_book = models.ForeignKey(MeritBadgeBook)
	date_requested = models.DateField(blank=True, null=True)
	date_borrowed = models.DateField(blank=True, null=True)
	date_due = models.DateField(blank=True, null=True)
	date_returned = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return '{0} - {1}'.format(self.scout, self.merit_badge_book)

class MeritBadgeCounselor(models.Model):
	scouter = models.ForeignKey(Scouter)
	merit_badge = models.ForeignKey(MeritBadge)
	date_requested = models.DateField(blank=True, null=True)
	date_started = models.DateField(blank=True, null=True)
	registered = models.BooleanField()
	active = models.BooleanField()

	def __unicode__(self):
		return '{0} - {1}'.format(self.scouter.user.username, self.merit_badge.name)
