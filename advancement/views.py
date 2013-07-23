from advancement import service
from advancement.models import Scouter, Rank, ScoutRank, ScoutMeritBadge, MeritBadge, ScoutNote
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import logging

logger = logging.getLogger(__name__)

def index(request):

	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@login_required
def home(request, scouter_id=None):
	user = request.user
	try:
		scouter = Scouter.objects.get(user=user)
		scouter_role = scouter.role
	except:
		scouter = None
		scouter_role = None

	if scouter_role == 'leader':
		scouts = Scouter.objects.filter(patrol=scouter.patrol).exclude(role='leader').order_by('user__first_name')
		if scouter.patrol == 'all':
			scouts = Scouter.objects.exclude(role='leader').order_by('user__first_name')
			
		scout = None
		if scouter_id:
			scout = Scouter.objects.get(id=scouter_id)

	else:
		scouts = []
		scout = scouter

	ranks = Rank.objects.all()
	scout_ranks = ScoutRank.objects.filter(scout=scout)

	scout_ranks_list = []
	for rank in ranks:
		scout_rank_dict = {'image_name': rank.image_name,
		                   'image_ph_name': rank.image_ph_name,
		                   'rank_id': rank.id,
		                   'rank_name': rank.name}
		for scout_rank in scout_ranks:
			if rank == scout_rank.rank:
				scout_rank_dict['id'] = scout_rank.id
				scout_rank_dict['date_earned'] = scout_rank.date_earned
				break
			
			else:
				scout_rank_dict['date_earned'] = None
		
		scout_ranks_list.append(scout_rank_dict)
	
	scout_merit_badges_earned = ScoutMeritBadge.objects.filter(scout=scout, date_earned__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')
	scout_merit_badges_planned = ScoutMeritBadge.objects.filter(scout=scout, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')

	scout_dict = {}
	if scout:
		scout_dict['name'] = '{0} {1}'.format(scout.user.first_name, scout.user.last_name)
		scout_dict['phone_number'] = scout.phone_number
		if scout.birth_date:
			age = service.get_birth_info(scout.birth_date, 'age')
			scout_dict['age'] = age
			scout_dict['turns_age'] = age + 1
			scout_dict['turns_month'] = service.get_birth_info(scout.birth_date, 'next_birthday').strftime('%b %d, %Y')

		scout_notes = []
		if scouter_role == 'leader':
			scout_notes = ScoutNote.objects.filter(scout=scout).order_by('-note_date')

	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def meritbadges(request):
	merit_badges = MeritBadge.objects.all().values_list('name', flat=True)
	
	return render_to_response('meritbadges.json', locals(), context_instance=RequestContext(request))

def update_scoutmeritbadge(request):
	if request.method == 'POST':
		action = request.POST.get('action')
		entry_type = request.POST.get('entry_type')
		if action == 'add':

			scout_id = request.POST.get('scout_id')
			mb_name = request.POST.get('mb_name')
			mb_date = datetime.strptime(request.POST.get('mb_date'), '%m/%d/%Y').strftime('%Y-%m-%d')

			merit_badge = MeritBadge.objects.get(name=mb_name)
			scout_merit_badge, created = ScoutMeritBadge.objects.get_or_create(scout_id=scout_id, merit_badge=merit_badge)
			if entry_type == 'earned':
				scout_merit_badge.date_earned = mb_date
				scout_merit_badge.goal_date = None
			elif entry_type == 'planned':
				if created:
					scout_merit_badge.goal_date = mb_date
			scout_merit_badge.save()

			merit_badge_json = json.dumps({'name': merit_badge.name,
				                           'mb_date': mb_date,
				                           'image_name': merit_badge.image_name,
				                           'scoutmeritbadge_id': scout_merit_badge.id,
				                           'created': created})

		if action == 'delete':
			scoutmeritbadge_id = request.POST.get('scout_merit_badge_id')
			ScoutMeritBadge.objects.get(id=scoutmeritbadge_id).delete()

			merit_badge_json = json.dumps({})

	return HttpResponse(merit_badge_json)

def ranks(request):
	ranks = Rank.objects.all().values_list('name', flat=True)
	
	return render_to_response('ranks.json', locals(), context_instance=RequestContext(request))

def update_scoutrank(request):
	if request.method == 'POST':
		action = request.POST.get('action')
		entry_type = request.POST.get('entry_type')
		if action == 'add':
			logger.debug('here1')

			scout_id = request.POST.get('scout_id')
			rank_name = request.POST.get('rank_name')
			rank_date = datetime.strptime(request.POST.get('rank_date'), '%m/%d/%Y').strftime('%Y-%m-%d')

			rank = Rank.objects.get(name=rank_name)
			scout_rank, created = ScoutRank.objects.get_or_create(scout_id=scout_id, rank=rank)
			scout_rank.date_earned = rank_date
			scout_rank.save()

			rank_json = json.dumps({'name': rank.name,
		                            'rank_date': rank_date,
		                            'image_name': rank.image_name,
		                            'image_ph_name': rank.image_ph_name,
		                            'scoutrank_id': scout_rank.id,
		                            'rank_id': rank.id,
		                            'created': created})

		if action == 'delete':
			logger.debug('here2')
			scoutrank_id = request.POST.get('scout_rank_id')
			scout_rank = ScoutRank.objects.get(id=scoutrank_id)
			rank = scout_rank.rank
			scout_rank.delete()

			rank_json = json.dumps({'rank_id': rank.id,
				                    'image_ph_name': rank.image_ph_name})

	return HttpResponse(rank_json)

