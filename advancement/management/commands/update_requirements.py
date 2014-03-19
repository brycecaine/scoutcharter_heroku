from advancement import service
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    help = 'Updates rank and merit-badge requirements from the scouting website.'

    # [('1', 'Hike'), ('2', 'Cook'), ('2a', 'Hamburgers'), ('2b', 'Potatoes'), ('3', 'Complete...'), ('3a', '

    def handle(self, *args, **options):
	r = requests.get('http://usscouts.org/advance/boyscout/bsrank2.asp')
	soup = BeautifulSoup(r.text)
	requirements_list = soup.find('ol')
	# requirements_list = requirements_div.find('ol').findAll('li')
	req_list = service.ol_to_list(requirements_list)
	for req in req_list:
	    print req

	"""
	for requirement in requirements_list:
		try:
			subreqs = requirement.find('ol').findAll('li')
			for subreq in subreqs:
				print " ".join(subreq.text.split())
		except:
			pass
			
		print " ".join(requirement.text.split())

	print requirement.escapeUnrecognizedEntities
	print requirement.name
	print requirement.parent
	print requirement.parserClass
	print requirement.convertHTMLEntities
	print requirement.nextSibling
	print requirement.next
	print requirement.isSelfClosing
	print requirement.convertXMLEntities
	print requirement.hidden
	print requirement.previous
	print requirement.previousSibling
	print requirement.containsSubstitutions
	print requirement.contents
	print requirement.attr
	"""
