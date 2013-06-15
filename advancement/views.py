from django.shortcuts import render_to_response
from django.template import RequestContext
from advancement.models import ScoutRank, ScoutMeritBadge

def home(request):
	# user = request.user
	# scout_ranks = ScoutRank.objects.filter(scout=user)
	# scout_merit_badges = ScoutMeritBadge.objects.filter(scout=user)

	
	
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))