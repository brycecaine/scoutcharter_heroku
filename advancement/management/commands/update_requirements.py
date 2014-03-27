from advancement import service
from advancement.models import Rank, MeritBadge, Requirement
from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    help = 'Updates rank and merit-badge requirements from the scouting website.'

    def handle(self, *args, **options):
        ranks = Rank.objects.all()
        for rank in ranks:
            print rank
            r = requests.get('http://usscouts.org/advance/boyscout/bsrank%s.asp' % rank.id)
            soup = BeautifulSoup(r.text)
            reqs_html_list = soup.find('ol')
            reqs_list = service.ol_to_list(reqs_html_list)

            req_objects = []
            for req in reqs_list:
                req['content_object'] = rank
                req_objects.append(Requirement(**req))
            
            Requirement.objects.bulk_create(req_objects)
            print '- rank done -'
        print '-- All ranks done --'

        """
        # Use the following for populating merit-badge requirements if needed
        merit_badges = MeritBadge.objects.all()
        for merit_badge in merit_badges:
            print merit_badge
            r = requests.get('http://usscouts.org/mb/mb%s.asp' % merit_badge.bsa_id)
            soup = BeautifulSoup(r.text)
            reqs_html_list = soup.find('ol')
            reqs_list = service.ol_to_list(reqs_html_list)

            req_objects = []
            for req in reqs_list:
                req['content_object'] = merit_badge
                req_objects.append(Requirement(**req))
            
            Requirement.objects.bulk_create(req_objects)
            print '- merit badge done -'
        print '-- All merit badges done --'
        """
