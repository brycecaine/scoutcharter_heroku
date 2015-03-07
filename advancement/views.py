from advancement import service
from advancement.models import Scouter, Parent, Rank, ScoutRank, ScoutMeritBadge, MeritBadge, ScoutNote, MeritBadgeBook, ScoutMeritBadgeBook, MeritBadgeCounselor, Requirement, ScoutRequirement
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from scoutcharter.forms import ScouterForm
import csv
import json
import logging
import random
import string

logger = logging.getLogger(__name__)

def index(request):

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@login_required
def home(request, scouter_id=None):
    user = request.user
    scouter = Scouter.objects.get(user=user)
    scout = None
    if scouter_id:
        scout = Scouter.objects.get(id=scouter_id)

    # -------------------------------------------------------------------------
    # Get list of scouts for leaders or parents
    scouts = service.get_scouts(scouter.role, scouter.patrol)
    scouts_by_age = scouts.order_by('birth_date')

    if scout not in scouts:
        scout = None

    scout_list = []
    for scout_item in scouts_by_age:
        scout_ranks = ScoutRank.objects.filter(scout=scout_item).order_by('-rank__weight')
        if scout_ranks:
            rank = scout_ranks[0].rank
        else:
            rank = '-'

        if scout_item.birth_date:
            age = service.get_birth_info(scout_item.birth_date, 'age')
        else:
            age = None

        mb_goals = ScoutMeritBadge.objects.filter(scout=scout_item, goal_date__gt='1901-01-01').order_by('-merit_badge__required', 'merit_badge__name').values_list('merit_badge__name', flat=True)
        
        scout_notes = ScoutNote.objects.filter(scout=scout_item).order_by('-note_date')
        if scout_notes:
            status = scout_notes[0]
        else:
            status = None
        scout_dict = {'id': scout_item.id,
                      'first_name': scout_item.user.first_name,
                      'last_name': scout_item.user.last_name,
                      'patrol': scout_item.patrol,
                      'rank': rank,
                      'age': age,
                      'birth_date': scout_item.birth_date,
                      'phone_number': scout_item.phone_number,
                      'mb_goals': 'Set' if mb_goals else '', # Change this if merit badges should appear in list
                      'status': status}
        scout_list.append(scout_dict)
            
    # -------------------------------------------------------------------------
    # Get other info if a scout is logged in
    if scouter.role == 'scout':
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
        scout_dict['username'] = scout.user.username
        scout_dict['phone_number'] = scout.phone_number
        if scout.birth_date:
            age = service.get_birth_info(scout.birth_date, 'age')
            scout_dict['age'] = age
            scout_dict['turns_age'] = age + 1
            scout_dict['turns_month'] = service.get_birth_info(scout.birth_date, 'next_birthday').strftime('%b %d, %Y')

        scout_notes = []
        if scouter.role == 'leader':
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
        scout_merit_badge_planned_dict = {'id': scout_merit_badge_planned.id,
                                          'merit_badge': scout_merit_badge_planned.merit_badge,
                                          'goal_date': scout_merit_badge_planned.goal_date}
        try:
            merit_badge_book = MeritBadgeBook.objects.get(merit_badge=scout_merit_badge_planned.merit_badge)
            scout_merit_badge_planned_dict['book_in_library'] = merit_badge_book.in_library
        except:
            scout_merit_badge_planned_dict['book_in_library'] = False
        
        for scout_merit_badge_book_planned in scout_merit_badge_books_planned:
            if scout_merit_badge_book_planned.merit_badge_book.merit_badge == scout_merit_badge_planned.merit_badge:
                scout_merit_badge_planned_dict['book_date_requested'] = scout_merit_badge_book_planned.date_requested
                scout_merit_badge_planned_dict['book_date_borrowed'] = scout_merit_badge_book_planned.date_borrowed
                scout_merit_badge_planned_dict['book_date_due'] = scout_merit_badge_book_planned.date_due

            else:
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
    rank_json = None
    if request.method == 'POST':
        action = request.POST.get('action')
        entry_type = request.POST.get('entry_type')
        if action == 'add':
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
        merit_badge_book = MeritBadgeBook.objects.get(merit_badge=merit_badge)
    except MeritBadgeBook.DoesNotExist:
        merit_badge_book = MeritBadgeBook.objects.create(merit_badge=merit_badge, owner='TBD', quantity=0)

    try:
        scout_merit_badge_book = ScoutMeritBadgeBook.objects.get(scout=scout, merit_badge_book=merit_badge_book)
        if scout_merit_badge_book.date_returned:
            scout_merit_badge_book = ScoutMeritBadgeBook.objects.create(scout=scout, merit_badge_book=merit_badge_book)
    except:
        scout_merit_badge_book = ScoutMeritBadgeBook.objects.create(scout=scout, merit_badge_book=merit_badge_book)

    scout_merit_badge_book.date_requested = datetime.now()
    scout_merit_badge_book.save()
    outcome = '<div>Book requested, you will be contacted soon</div>'

    # Email admin
    mbbook_admin_group = Group.objects.get(name='mbbook_admin')
    mbbook_admin_emails = mbbook_admin_group.user_set.all().values_list('email', flat=True)
    send_mail('Merit badge book requested: %s' % merit_badge, '%s has requested the %s merit badge book.' % (scout_merit_badge_book.scout, merit_badge), 'admin@scoutcharter.com', mbbook_admin_emails, fail_silently=False) 

    return_json = json.dumps({'outcome': outcome})

    return HttpResponse(return_json)

def view_mbcounselors(request, meritbadge_id=None):
    merit_badge = MeritBadge.objects.get(id=meritbadge_id)
    merit_badge_counselors = MeritBadgeCounselor.objects.filter(merit_badge=merit_badge)

    return render_to_response('mbcounselors.html', locals(), context_instance=RequestContext(request))

def export(request):
    today_string = datetime.now().strftime('%Y%m%d')
    now_string = datetime.now().strftime('%H%M%S')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')

    # Get list of ranks earned within date range
    scout_ranks = ScoutRank.objects.filter(date_earned__range=(from_date, to_date))

    # Get list of merit badges earned within date range
    scout_merit_badges = ScoutMeritBadge.objects.filter(date_earned__range=(from_date, to_date))

    # Return as csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ADVS1886.CSV"' # Not sure if this has to be the exact file name or not

    header_1 = ['001',
                '1',
                'A',
                today_string,
                now_string,
                'ScoutCharter', # 'TroopMaster ME' changed to ScoutCharter
                '02.00', # ?
                None]

    header_2 = ['020',
                '2',
                'Troop', # unit level
                '1886', # unit id
                '201401', # year-month of charter expiration
                'Cedar Breaks', # district name
                'Cedar City', # city
                'UT', # state
                '84721', # zip
                'Valley View Ward', # charter organization
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                today_string,
                today_string,
                today_string,
                None]

    writer = csv.writer(response, delimiter=',')

    writer.writerow(header_1)
    writer.writerow(header_2)
    
    i = 0
    for i, scout_merit_badge in enumerate(scout_merit_badges, start=3):
        # Need to figure out the merit badge ids and the 021
        row_dict = ['021',
                    i,
                    scout_merit_badge.scout.user.first_name,
                    None,
                    scout_merit_badge.scout.user.last_name,
                    scout_merit_badge.scout.birth_date.strftime('%Y%m%d'),
                    None,
                    scout_merit_badge.date_earned.strftime('%Y%m%d'),
                    scout_merit_badge.merit_badge.bsa_id,
                    None]
        writer.writerow(row_dict)

    j = 0
    for j, scout_rank in enumerate(scout_ranks, start=i+1):
        # Need to figure out the rank ids and the 021
        row_dict = ['021',
                    j,
                    scout_rank.scout.user.first_name,
                    None,
                    scout_rank.scout.user.last_name,
                    scout_rank.scout.birth_date.strftime('%Y%m%d'),
                    None,
                    scout_rank.date_earned.strftime('%Y%m%d'),
                    scout_rank.rank.bsa_id,
                    None]
        writer.writerow(row_dict)

    writer.writerow(['900',
                     j + 1,
                     None])

    return response

@login_required
def edit_scouter(request, username=None):
    user = request.user
    scouter = Scouter.objects.get(user=user)
    user_to_edit = None
    scouter_to_edit = Scouter()
    form_dict = {}
    mode = 'A'

    if username:
        user_to_edit = User.objects.get(username=username)
        scouter_to_edit = Scouter.objects.get(user=user_to_edit)

        if ((scouter.role == 'leader' and scouter_to_edit.role == 'scout') or
            scouter == scouter_to_edit):

            form_dict = {'first_name': scouter_to_edit.user.first_name,
                         'last_name': scouter_to_edit.user.last_name,
                         'email': scouter_to_edit.user.email,
                         'username': scouter_to_edit.user.username,
                         'phone_number': scouter_to_edit.phone_number,
                         'birth_date': scouter_to_edit.birth_date,
                         'role': scouter_to_edit.role,
                         'patrol': scouter_to_edit.patrol,
                         'rank': scouter_to_edit.rank}
            mode = 'E'

    next_path = request.GET.get('next')

    if request.method == 'POST':
        form = ScouterForm(username, mode, request.POST)

        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_email = form.cleaned_data['email']
            if mode == 'A':
                password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
                user_to_edit = User.objects.create_user(form_username, form_email, password)
            else:
                user_to_edit.username = form_username
                user_to_edit.email = form_email
            user_to_edit.first_name = form.cleaned_data['first_name']
            user_to_edit.last_name = form.cleaned_data['last_name']
            user_to_edit.save()

            scouter_to_edit.user = user_to_edit
            scouter_to_edit.phone_number = form.cleaned_data['phone_number']
            scouter_to_edit.birth_date = form.cleaned_data['birth_date']
            scouter_to_edit.role = form.cleaned_data['role']
            scouter_to_edit.patrol = form.cleaned_data['patrol']
            scouter_to_edit.rank = form.cleaned_data['rank']
            scouter_to_edit.save()

            send_mail('Your New ScoutCharter Account', 'One of your scout leaders has created your ScoutCharter account. Please log in with the username %s and password %s' % (form_username, password), 'admin@scoutcharter.com', [form_email], fail_silently=False)

            # return render_to_response("registration/cadastro_concluido.html",{})
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
        else:
            return render_to_response('registration/edit_scouter.html', locals(), context_instance=RequestContext(request))

    else:    
        form = ScouterForm(username, mode, initial=form_dict)
        # return render_to_response("registration/registration.html", {'form': form})
        return render_to_response('registration/edit_scouter.html', locals(), context_instance=RequestContext(request))

def rank_requirements(request, scoutrank_id=None):
    user = request.user
    scouter = Scouter.objects.get(user=user)
    scouter_role = scouter.role

    scouts = service.get_scouts(scouter.role, scouter.patrol)

    if scoutrank_id:
        scout_rank = ScoutRank.objects.get(id=scoutrank_id)
        scout = scout_rank.scout
        rank = scout_rank.rank
    else:
        scout_id = request.GET.get('scout_id')
        scout = Scouter.objects.get(id=scout_id)
        rank_id = request.GET.get('rank_id')
        rank = Rank.objects.get(id=rank_id)
        scout_rank, created = ScoutRank.objects.get_or_create(scout=scout, rank=rank)

    rank_type = ContentType.objects.get_for_model(Rank)
    rank_requirements = Requirement.objects.filter(content_type=rank_type, object_id=rank.id)
    rank_requirements_dict = rank_requirements.values()

    scout_rankreqs = ScoutRequirement.objects.filter(scout=scout, requirement__in=rank_requirements)

    scout_rankreq_dict = {}
    for scout_rankreq in scout_rankreqs:
        scout_rankreq_dict[scout_rankreq.requirement.id] = scout_rankreq.date_completed

    rank_requirements_list = []
    for rank_requirement in rank_requirements_dict:
        rank_requirement['date_completed'] = scout_rankreq_dict.get(rank_requirement['id'], None)
        rank_requirements_list.append(rank_requirement)

    if request.method == 'POST':
        # Loop over form fields
        for key, value in request.POST.dict().items():
            if 'rankreq-date-name' in key:
                scout_id = key.split('-')[-2]
                rank_requirement_id = key.split('-')[-1]

                # Update each scout requirement
                scout_rankreq, created = ScoutRequirement.objects.get_or_create(scout_id=scout_id, requirement_id=rank_requirement_id) 
                if value:
                    scout_rankreq.date_completed = datetime.strptime(value, '%m/%d/%Y')
                else:
                    scout_rankreq.date_completed = None
                scout_rankreq.leader = scouter
                scout_rankreq.save()
        return HttpResponseRedirect('/home/scout/' + str(scout.id))

    return render_to_response('rank-requirements.html', locals(), context_instance=RequestContext(request))

def signup(request):
    return render_to_response('signup.html', locals(), context_instance=RequestContext(request))

def custom_404(request):
    return render(request, '404.html')

def custom_500(request):
    return render(request, '500.html')

@login_required
def report_list(request):
    user = request.user
    scouter = Scouter.objects.get(user=user)

    scouts = service.get_scouts(scouter.role, scouter.patrol)
    scouts_by_age = scouts.order_by('birth_date') # Need to fix this so the order_by doesn't happen twice

    response = HttpResponse(content_type='application/pdf')
    # Uncommenting this line downloads the pdf rather than displaying it in the browser
    # response['Content-Disposition'] = 'attachment; filename="Scout List.pdf"'

    p = canvas.Canvas(response)

    # -------------------------------------------------------------------------
    # Draw the pdf report
    x = 1 * inch
    y = 10.5 * inch

    for scout in scouts_by_age:
        scout_name = '%s %s' % (scout.user.first_name, scout.user.last_name)
        scout_birth_date = ''
        if scout.birth_date:
            scout_birth_date = scout.birth_date.strftime("%B %d, %Y")

        scout_rank = ''
        if scout.rank:
            scout_rank = scout.rank

        p.drawString(x, y, scout_name)
        p.drawString(3 * x, y, scout_rank)
        p.drawString(5 * x, y, scout_birth_date) 

        y -= 0.2 * inch

    p.showPage()
    p.save()

    return response

@login_required
def report_scout(request, scouter_id=None):
    user = request.user
    scouter = Scouter.objects.get(user=user)

    scouts = service.get_scouts(scouter.role, scouter.patrol)
    scouts_by_age = scouts.order_by('birth_date')
    if scouter_id:
        scouts_by_age = scouts_by_age.filter(id=scouter_id)

    response = HttpResponse(content_type='application/pdf')
    # Uncommenting this line downloads the pdf rather than displaying it in the browser
    # response['Content-Disposition'] = 'attachment; filename="Scout List.pdf"'

    p = canvas.Canvas(response)

    # -------------------------------------------------------------------------
    # Draw the pdf report
    for scout in scouts_by_age:
        x = 1 * inch
        y = 10.5 * inch
        scout_name = '%s %s' % (scout.user.first_name, scout.user.last_name)
        scout_birth_date = ''
        if scout.birth_date:
            scout_birth_date = scout.birth_date.strftime("%B %d, %Y")

        p.drawString(x, y, scout_name)
        p.drawString(5 * x, y, scout_birth_date) 

        y -= 0.4 * inch

        # ---------------------------------------------------------------------
        # List Ranks
        p.drawString(x, y, '------ Ranks ------')
        y -= 0.2 * inch
        scout_ranks = ScoutRank.objects.filter(scout=scout)
        if not scout_ranks:
            p.drawString(x, y, 'No ranks found')
            y -= 0.2 * inch
            
        for scout_rank in scout_ranks:
            p.drawString(x, y, scout_rank.rank.name)
            if scout_rank.date_earned:
                p.drawString(5 * x, y, scout_rank.date_earned.strftime("%B %d, %Y"))
            y -= 0.2 * inch

        y -= 0.2 * inch

        # ---------------------------------------------------------------------
        # List Merit Badges
        p.drawString(x, y, '------ Merit Badges ------')
        y -= 0.2 * inch
        scout_merit_badges = ScoutMeritBadge.objects.filter(scout=scout)
        if not scout_merit_badges:
            p.drawString(x, y, 'No merit badges found')
            y -= 0.2 * inch
            
        for scout_merit_badge in scout_merit_badges:
            p.drawString(x, y, scout_merit_badge.merit_badge.name)
            if scout_merit_badge.date_earned:
                p.drawString(5 * x, y, scout_merit_badge.date_earned.strftime("%B %d, %Y"))
            y -= 0.2 * inch

        y -= 0.4 * inch

        p.showPage()
    p.save()

    return response
