from django.shortcuts import render_to_response
from django.template import RequestContext
from advancement.models import Scouter, ScoutRank, ScoutMeritBadge

def home(request):
	user = request.user
	scouter = Scouter.objects.get(user=user)
	scout_ranks = ScoutRank.objects.filter(scout=scouter)
	scout_merit_badges_earned = ScoutMeritBadge.objects.filter(scout=scouter, date_earned__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')
	scout_merit_badges_planned = ScoutMeritBadge.objects.filter(scout=scouter, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name')

	return render_to_response('index.html', locals(), context_instance=RequestContext(request))