from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user

from .models import *
from .forms import *

def home(request):
	return render(request, 'home.html')

def login(request):
	context = {}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login_user(request, user)
			return redirect(request.POST.get('next'))
		else:
			context['error'] = "Usuário ou senha inválidos."
			context['username'] = username

	return render(request, 'login.html', context)

def logout(request):
	logout_user(request)
	return redirect('/')

def about(request):
	return render(request,'about.html',{})

def tournaments(request):
	context = {
		'title': 'Torneios',
		'tournaments': Tournament.objects.all(),
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios'},
		]
	}
	return render(request, 'tournaments.html', context)

@login_required()
def add_tournament(request):
	if request.method == 'POST':
		form = TournamentForm(request.POST)
		if form.is_valid():
			tournament = form.save()
			return redirect('/torneios/' + str(tournament.id))
	else:
		form = TournamentForm()

	context = {
		'title': "Novo Torneio",
		'action': '/torneios/novo',
		'cancel': '/torneios',
		'form': form,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': 'Novo'},
		]
	}

	return render(request, 'form.html', context)

def tournament_details(request, tournament_id):
	tournament = get_object_or_404(Tournament, id=tournament_id)
	context = {
		'title': 'Torneio',
		'tournament': tournament,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': 'Torneio'},
		]
	}

	return render(request, 'tournament-details.html', context)

@login_required()
def edit_tournament(request, tournament_id):
	tournament = get_object_or_404(Tournament, id=tournament_id)
	if request.method == 'POST':
		form = TournamentForm(request.POST, instance=tournament)
		if form.is_valid():
			form.save()
			return redirect('/torneios')
	else:
		form = TournamentForm(instance=tournament)

	context = {
		'title': "Editar Torneio",
		'action': '/torneios/editar/' + tournament_id,
		'cancel': '/torneios/' + tournament_id,
		'form': form,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': tournament, 'link': '/torneios/' + tournament_id},
			{'name': 'Editar'},
		]
	}

	return render(request, 'form.html', context)

@login_required()
def remove_tournament(request, tournament_id):
	get_object_or_404(Tournament, id=tournament_id).delete()
	return redirect('/torneios')

@login_required()
def add_competition(request, tournament_id):
	if request.method == 'POST':
		form = CompetitionForm(request.POST, tournament_id)
		if form.is_valid():
			competition = form.save(commit=False)
			competition.tournament = Tournament.objects.get(id=tournament_id)
			competition.save()
			return redirect('/competicoes/' + str(competition.id))

	else:
		form = CompetitionForm()

	tournament = get_object_or_404(Tournament, id=tournament_id)
	context = {
		'title': "Nova Competição",
		'action': '/competicoes/novo/' + tournament_id,
		'cancel': '/torneios/' + tournament_id,
		'form': form,
		'tournament' : tournament,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': tournament, 'link': '/torneios/' + tournament_id},
			{'name': 'Competições', 'link': '/torneios/' + tournament_id},
			{'name': 'Nova'},
		]
	}

	return render(request, 'form.html', context)

def competition_details(request, competition_id):
	competition = get_object_or_404(Competition, id=competition_id)
	tournament = competition.tournament
	context = {
		'title': competition,
		'competition': competition,
		'tournament': tournament,
		'trials': competition.matches.filter(intercampi=False),
		'intercampi': Match.objects.filter(competition=competition, intercampi=True).first(),
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': tournament, 'link': '/torneios/' + str(tournament.id)},
			{'name': "Competições", 'link': '/torneios/' + str(tournament.id)},
			{'name': competition.category },
		]
	}

	return render(request, 'competition-details.html', context)

@login_required()
def edit_competition(request, competition_id):
	pass

@login_required()
def add_match(request, competition_id):
	if request.method == 'POST':
		form = MatchForm(request.POST)
		if form.is_valid():
			match = form.save(commit=False)
			match.intercampi = request.POST['intercampi']
			match.competition = Competition.objects.get(id=competition_id)
			match.save()
			return redirect('/competicoes/' + competition_id)
	else:
		form = MatchForm(initial={'data': '', 'inicio': '', 'termino': ''})

	competition = get_object_or_404(Competition, id=competition_id)
	context = {
		'title': 'Nova Final' if request.GET.get('intercampi') else 'Nova Seletiva',
		'action': '/jogos/novo/' + competition_id,
		'cancel': '/competicoes/' + competition_id,
		'competition': competition,
		'form': form,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': competition.tournament, 'link': '/torneios/' + str(competition.tournament.id)},
			{'name': 'Competições', 'link': '/torneios'},
			{'name': competition, 'link': '/competicoes/' + str(competition.id)},
			{'name': 'Novo'},
		]
	}

	return render(request, 'form.html', context)

def match_details(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	context = {
		'title': match.type() + ' - ' + str(match.competition),
		'match': match,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': match.competition.tournament, 'link': '/torneios/' + str(match.competition.tournament.id)},
			{'name': 'Competições', 'link': '/torneios'},
			{'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
			{'name': match.type() },
		]
	}

	return render(request, 'match-details.html', context)

@login_required()
def edit_match(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	if request.method == 'POST':
		form = MatchForm(request.POST, instance=match)
		if form.is_valid():
			form.save()
			return redirect('/jogos/' + match_id)
	else:
		form = MatchForm(instance=match)

	competition = get_object_or_404(Competition, id=match.competition.id)
	context = {
		'title': "Editar " + match.type(),
		'action': '/competicoes/editar/' + match_id,
		'cancel': '/competicoes/' + match_id,
		'competition': competition,
		'form': form,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': match.competition.tournament, 'link': '/torneios/' + str(match.competition.tournament.id)},
			{'name': 'Competições', 'link': '/torneios'},
			{'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
			{'name': match.type(), 'link': '/competicoes/' + str(match.id) },
			{'name': 'Editar'},
		]
	}
	
	return render(request, 'form.html', context)

@login_required()
def remove_match(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	competition_id = match.competition.id
	match.delete()
	return redirect('/competicoes/' + str(competition_id))

def attend_to_match(request, match_id):
	import pdb; pdb.set_trace()
	match = get_object_or_404(Match, id=match_id)
	competition = match.competition

	if request.method == 'POST':
		form = AttendForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			code = form.cleaned_data['code']
			email = form.cleaned_data['email']
			course = form.cleaned_data['course']
			participant = Participant.objects.create(name=name, code=code, email=email, course=course)
			MatchScore.objects.create(match=match, participant=participant)
			match.participants.add(participant)
			return redirect('/jogos/' + match_id)
	else:
		form = AttendForm()

	context = {
		'title': "Participar " + match.type(),
		'action': '/jogos/participar/' + match_id,
		'cancel': '/jogos/' + match_id,
		'competition': competition,
		'form': form,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': match.competition.tournament, 'link': '/torneios/' + str(match.competition.tournament.id)},
			{'name': 'Competições', 'link': '/torneios'},
			{'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
			{'name': match.type(), 'link': '/jogos/' + str(match.id) },
			{'name': 'Participar'},
		]
	}
	
	return render(request, 'form.html', context)

@login_required()
def leave_match(request, match_id):
	match = get_object_or_404(Match, id=match_id)
	match.participants.remove(request.user)
	score = MatchScore.objects.get(match=match, participant=request.user)
	score.delete()
	return redirect('/jogos/' + str(match_id))

@login_required()
def update_score(request, match_id):
	match = get_object_or_404(Match, id=match_id)

	if request.method == 'POST':
		for score in match.scores.all():
			p = request.POST.getlist(str(score.id))
			score.pontos = p[0]
			score.tempo = p[1]
			score.save()

		return redirect('/jogos/' + str(match_id))

	context = {
		'title': 'Atualizar Pontuação',
		'match': match,
		'breadcrumb': [
			{'name': 'Início', 'link': '/'},
			{'name': 'Torneios', 'link': '/torneios'},
			{'name': match.competition.tournament, 'link': '/torneios/' + str(match.competition.tournament.id)},
			{'name': 'Jogos', 'link': '/competicoes/' + str(match.competition.id)},
			{'name': 'Atualizar'},
		]
	}

	return render(request, 'update-score.html', context)	
