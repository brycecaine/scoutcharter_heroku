from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Patrol(models.Model):
	kind = models.CharField(max_length=30) # troop, team, crew


class Rank(models.Model):
	bsa_id = models.CharField(max_length=10)
	weight = models.IntegerField()
	name = models.CharField(max_length=30)
	number_required_meritbadges = models.IntegerField()
	number_optional_meritbadges = models.IntegerField()
	image_name = models.CharField(max_length=200, blank=True, null=True)
	image_ph_name = models.CharField(max_length=200, blank=True, null=True)

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
		return '{0} {1}'.format(self.user.first_name, self.user.last_name)

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
	bsa_id = models.CharField(max_length=10)
	name = models.CharField(max_length=100)
	required = models.BooleanField()
	alternates = models.CharField(max_length=200, blank=True, null=True)
	image_name = models.CharField(max_length=200, blank=True, null=True)

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
	in_library = models.BooleanField()

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
		return '{0} - {1}'.format(self.scouter, self.merit_badge.name)

class ScoutNote(models.Model):
	scout = models.ForeignKey(Scouter, related_name='scoutnote_scout')
	leader = models.ForeignKey(Scouter, related_name='scoutnote_leader')
	note_date = models.DateField(blank=True, null=True)
	method = models.CharField(max_length=30, blank=True, null=True)
	purpose = models.CharField(max_length=500, blank=True, null=True)
	comment = models.CharField(max_length=1500)
	followup_date = models.DateField(blank=True, null=True)

	def __unicode__(self):
		return '{0}: {1} (Followup on {2})'.format(self.note_date, self.comment, self.followup_date)

class Requirement(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	number = models.CharField(max_length=10)
	description = models.TextField()
	is_header = models.BooleanField()

	def __unicode__(self):
		return '{0}: {1}. {2}'.format(self.content_object, self.number, self.description)

class ScoutRequirement(models.Model):
	scout = models.ForeignKey(Scouter, related_name='scoutrequirement_scout')
	requirement = models.ForeignKey(Requirement)
	date_completed = models.DateField(blank=True, null=True)
	leader = models.ForeignKey(Scouter, related_name='scoutrequirement_leader', blank=True, null=True)

	def __unicode__(self):
		return '{0}: {1} - {2}'.format(self.scout, self.requirement, self.date_completed)
