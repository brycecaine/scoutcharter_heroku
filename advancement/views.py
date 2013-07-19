from advancement.models import Scouter, Rank, ScoutRank, ScoutMeritBadge
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def home(request):
	user = request.user
	scouter = Scouter.objects.get(user=user)
	ranks = Rank.objects.all()
	scout_ranks = ScoutRank.objects.filter(scout=scouter)

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
	
	scout_merit_badges_earned = ScoutMeritBadge.objects.filter(scout=scouter, date_earned__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')
	scout_merit_badges_planned = ScoutMeritBadge.objects.filter(scout=scouter, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')

	return render_to_response('index.html', locals(), context_instance=RequestContext(request))