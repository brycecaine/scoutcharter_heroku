from advancement import service
from advancement.models import Scouter, Parent, Rank, ScoutRank, ScoutMeritBadge, MeritBadge, ScoutNote, MeritBadgeBook, ScoutMeritBadgeBook, MeritBadgeCounselor
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import csv
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

	# -------------------------------------------------------------------------
	# Get list of scouts for leaders or parents
	scouts_by_age = []
	if scouter_role == 'leader':
		scouts = Scouter.objects.filter(patrol=scouter.patrol).exclude(role='leader').order_by('user__first_name')
		if scouter.patrol == 'all':
			scouts = Scouter.objects.exclude(role='leader').order_by('user__first_name')
			scouts_by_age = scouts.order_by('birth_date') # Need to fix this so the order_by doesn't happen twice

		scout = None
		if scouter_id:
			scout = Scouter.objects.get(id=scouter_id)

	elif scouter_role == 'parent':
		parent = Parent.objects.get(user=user)
		scouts = parent.scouts.all()
		scouts_by_age = scouts.order_by('birth_date')

	scout_list = []
	for scout in scouts_by_age:
		scout_ranks = ScoutRank.objects.filter(scout=scout).order_by('-rank__weight')
		if scout_ranks:
			rank = scout_ranks[0].rank
		else:
			rank = '-'

		if scout.birth_date:
			age = service.get_birth_info(scout.birth_date, 'age')
		else:
			age = None

		mb_goals = ScoutMeritBadge.objects.filter(scout=scout, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name').values_list('merit_badge__name', flat=True)
		
		scout_notes = ScoutNote.objects.filter(scout=scout).order_by('-note_date')
		if scout_notes:
			status = scout_notes[0]
		else:
			status = None
		scout_dict = {'id': scout.id,
		              'first_name': scout.user.first_name,
		              'last_name': scout.user.last_name,
		              'patrol': scout.patrol,
		              'rank': rank,
		              'age': age,
		              'birth_date': scout.birth_date,
		              'phone_number': scout.phone_number,
		              'mb_goals': 'Set' if mb_goals else '', # Change this if merit badges should appear in list
		              'status': status}
		scout_list.append(scout_dict)
			
		scout = None
		if scouter_id:
			scout = Scouter.objects.get(id=scouter_id)


	# -------------------------------------------------------------------------
	# Get other info if a scout is logged in
	if scouter_role == 'scout':
		scout_list = []
		scout = scouter

	# -------------------------------------------------------------------------
	# Get ranks
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
	
	# -------------------------------------------------------------------------
	# Get merit badges
	scout_merit_badges_earned = ScoutMeritBadge.objects.filter(scout=scout, date_earned__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')
	scout_merit_badges_planned = ScoutMeritBadge.objects.filter(scout=scout, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')

	# -------------------------------------------------------------------------
	# Get individual scout info
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

	# -------------------------------------------------------------------------
	# Get merit-badge book info
	scout_merit_badge_books = ScoutMeritBadgeBook.objects.filter(scout=scout).exclude(date_returned__gt='1901-01-01')
	scout_merit_badges_planned_mbs = scout_merit_badges_planned.values_list('merit_badge', flat=True)

	scout_merit_badge_books_planned = []
	scout_merit_badge_books_unplanned = []
	for scout_merit_badge_book in scout_merit_badge_books:
		if scout_merit_badge_book.merit_badge_book.merit_badge.id in scout_merit_badges_planned_mbs:
			scout_merit_badge_books_planned.append(scout_merit_badge_book)
		
		elif scout_merit_badge_book.date_borrowed:
			scout_merit_badge_books_unplanned.append(scout_merit_badge_book)

	scout_merit_badges_planned_list = []
	for scout_merit_badge_planned in scout_merit_badges_planned:
		logging.error(1)
		scout_merit_badge_planned_dict = {'id': scout_merit_badge_planned.id,
		                                  'merit_badge': scout_merit_badge_planned.merit_badge,
		                                  'goal_date': scout_merit_badge_planned.goal_date}
		for scout_merit_badge_book_planned in scout_merit_badge_books_planned:
			logging.error(2)
			if scout_merit_badge_book_planned.merit_badge_book.merit_badge == scout_merit_badge_planned.merit_badge:
				logging.error(3)
				scout_merit_badge_planned_dict['book_in_library'] = True
				scout_merit_badge_planned_dict['book_date_requested'] = scout_merit_badge_book_planned.date_requested
				scout_merit_badge_planned_dict['book_date_borrowed'] = scout_merit_badge_book_planned.date_borrowed
				scout_merit_badge_planned_dict['book_date_due'] = scout_merit_badge_book_planned.date_due

			else:
				scout_merit_badge_planned_dict['book_in_library'] = False
				scout_merit_badge_planned_dict['book_date_requested'] = None
				scout_merit_badge_planned_dict['book_date_borrowed'] = None
				scout_merit_badge_planned_dict['book_date_due'] = None

		scout_merit_badges_planned_list.append(scout_merit_badge_planned_dict)

	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def meritbadges(request):
	search_key = request.GET.get('q', '')
	merit_badges = MeritBadge.objects.filter(name__icontains=search_key).values_list('name', flat=True)
	
	return render_to_response('meritbadges.json', locals(), context_instance=RequestContext(request))

def update_scoutmeritbadge(request):
	if request.method == 'POST':
		action = request.POST.get('action')
		entry_type = request.POST.get('entry_type')
		merit_badge_json = json.dumps({})
		if action == 'add':
			user = request.user
			scouter = Scouter.objects.get(user=user)
			
			if scouter.role in ('leader', 'parent'):
				scout_id = request.POST.get('scout_id')
				scout = Scouter.objects.get(id=scout_id)
			
			else:
				scout = scouter
			
			mb_name = request.POST.get('mb_name')
			mb_date = datetime.strptime(request.POST.get('mb_date'), '%m/%d/%Y').strftime('%Y-%m-%d')

			merit_badge = MeritBadge.objects.get(name=mb_name)
			scout_merit_badge, created = ScoutMeritBadge.objects.get_or_create(scout=scout, merit_badge=merit_badge)
			
			try:
				merit_badge_book = MeritBadgeBook.objects.get(merit_badge=merit_badge)
			except MeritBadgeBook.DoesNotExist:
				merit_badge_book = None
			
			try:
				scout_merit_badge_book = ScoutMeritBadgeBook.objects.get(scout=scout, merit_badge_book=merit_badge_book)
			except ScoutMeritBadgeBook.DoesNotExist:
				scout_merit_badge_book = None

			if entry_type == 'earned':
				scout_merit_badge.date_earned = mb_date
				scout_merit_badge.goal_date = None
			
			elif entry_type == 'planned':
				if created:
					scout_merit_badge.goal_date = mb_date
			scout_merit_badge.save()

			planned_mb_dict = {'name': merit_badge.name,
				               'mb_date': mb_date,
				               'image_name': merit_badge.image_name,
				               'scoutmeritbadge_id': scout_merit_badge.id,
				               'meritbadge_id': scout_merit_badge.merit_badge.id,
				               'created': created,
				               'book_in_library': None,
				               'book_date_requested': None,
				               'book_date_borrowed': None,
				               'book_date_due': None}

			if merit_badge_book:
				planned_mb_dict['book_in_library'] = merit_badge_book.in_library

			if scout_merit_badge_book:
				planned_mb_dict['book_date_requested'] = scout_merit_badge_book.date_requested
				planned_mb_dict['book_date_borrowed'] = scout_merit_badge_book.date_borrowed
				planned_mb_dict['book_date_due'] = scout_merit_badge_book.date_due

			merit_badge_json = json.dumps(planned_mb_dict)

		if action == 'delete':
			scoutmeritbadge_id = request.POST.get('scout_merit_badge_id')
			ScoutMeritBadge.objects.get(id=scoutmeritbadge_id).delete()

			merit_badge_json = json.dumps({})

	return HttpResponse(merit_badge_json)

def ranks(request):
	search_key = request.GET.get('q', '')
	ranks = Rank.objects.filter(name__icontains=search_key).values_list('name', flat=True)
	
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

def request_mbbook(request):
	# Create mb book request in the database
	user = request.user
	scout = Scouter.objects.get(user=user)

	meritbadge_id = request.POST.get('meritbadge_id')
	merit_badge = MeritBadge.objects.get(id=meritbadge_id)
	
	try:
		logging.error(0)
		merit_badge_book = MeritBadgeBook.objects.get(merit_badge=merit_badge)
		logging.error(1)
	except:
		outcome = '<div>Merit badge book not in library</div>'

	try:
		scout_merit_badge_book = ScoutMeritBadgeBook.objects.get(scout=scout, merit_badge_book=merit_badge_book)
		if scout_merit_badge_book.date_returned:
			scout_merit_badge_book = ScoutMeritBadgeBook.objects.create(scout=scout, merit_badge_book=merit_badge_book)
	except:
		scout_merit_badge_book = ScoutMeritBadgeBook.objects.create(scout=scout, merit_badge_book=merit_badge_book)

	scout_merit_badge_book = ScoutMeritBadgeBook.objects.create(scout=scout, merit_badge_book=merit_badge_book)
	
	logging.error(2)
	scout_merit_badge_book.date_requested = datetime.now()
	logging.error(3)
	scout_merit_badge_book.save()
	logging.error(4)
	outcome = '<div>Book requested, you will be contacted soon</div>'
	logging.error(5)

	# Email admin
	# Add functionality to notify the admin of this request

	return_json = json.dumps({'outcome': outcome})

	return HttpResponse(return_json)

def view_mbcounselors(request, meritbadge_id=None):
	merit_badge = MeritBadge.objects.get(id=meritbadge_id)
	merit_badge_counselors = MeritBadgeCounselor.objects.filter(merit_badge=merit_badge)

	return render_to_response('mbcounselors.html', locals(), context_instance=RequestContext(request))

def export(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')

    # Get list of ranks earned within date range
    scout_ranks = ScoutRank.objects.filter(date_earned__range=(from_date, to_date))

    # Get list of merit badges earned within date range
    scout_merit_badges = ScoutMeritBadge.objects.filter(date_earned__range=(from_date, to_date))

    # Return as csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ADVS1886.CSV"' # Not sure if this has to be the exact file name or not

    writer = csv.writer(response)
    writer.writerow('001,1,A,20130824,222151,ScoutCharter,02.00,'.split(',')) # 'TroopMaster ME' changed to ScoutCharter
    writer.writerow('020,2,Troop,1886,201401,Cedar Breaks,Cedar City,UT,84721,Valley View Ward,,,,,,,,,,,,,,,,,,,,20130824,20130829,20130824,'.split(','))
    
    i = 0
    for i, scout_merit_badge in enumerate(scout_merit_badges, start=3):
    	# Need to figure out the merit badge ids and the 021
    	row_list = ['021', i, scout_merit_badge.scout.user.first_name, None, scout_merit_badge.scout.user.first_name, scout_merit_badge.scout.birth_date.strftime('%Y%m%d'), None, scout_merit_badge.date_earned.strftime('%Y%m%d'), '033', None]
    	writer.writerow(row_list)

    for j, scout_rank in enumerate(scout_ranks, start=i+1):
    	# Need to figure out the rank ids and the 021
    	row_list = ['021', j, scout_rank.scout.user.first_name, None, scout_rank.scout.user.first_name, scout_rank.scout.birth_date.strftime('%Y%m%d'), None, scout_rank.date_earned.strftime('%Y%m%d'), 'RN', None]
    	writer.writerow(row_list)

    writer.writerow('900,6,'.split(','))

    return response
