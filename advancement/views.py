from advancement import service
from advancement.models import Scouter, Rank, ScoutRank, ScoutMeritBadge
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

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
		scout_rank_dict = {'image_name': '_'.join(rank.name.split(' ')).lower(),
		                   'rank_name': rank.name}
		for scout_rank in scout_ranks:
			if rank == scout_rank.rank:
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
		if scout.birth_date:
			age = service.get_birth_info(scout.birth_date, 'age')
			scout_dict['age'] = age
			scout_dict['turns_age'] = age + 1
			scout_dict['turns_month'] = service.get_birth_info(scout.birth_date, 'next_birthday').strftime('%b %d, %Y')

	return render_to_response('home.html', locals(), context_instance=RequestContext(request))