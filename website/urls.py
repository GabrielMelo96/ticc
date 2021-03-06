from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'login$', views.login),
	url(r'logout$', views.logout),
	url(r'sobre$',views.about),
	url(r'torneios$', views.tournaments),
	url(r'torneios/novo', views.add_tournament),
	url(r'torneios/(?P<tournament_id>[0-9]+)$', views.tournament_details),
	url(r'torneios/editar/(?P<tournament_id>[0-9]+)$', views.edit_tournament),
	url(r'torneios/excluir/(?P<tournament_id>[0-9]+)$', views.remove_tournament),

	url(r'competicoes/novo/(?P<tournament_id>[0-9]+)$', views.add_competition),
	url(r'competicoes/(?P<competition_id>[0-9]+)$', views.competition_details),
	url(r'competicoes/editar/(?P<competition_id>[0-9]+)$', views.edit_competition),
	
	url(r'jogos/(?P<match_id>[0-9]+)$', views.match_details),
	url(r'jogos/novo/(?P<competition_id>[0-9]+)$', views.add_match),
	url(r'jogos/editar/(?P<match_id>[0-9]+)$', views.edit_match),
	url(r'jogos/excluir/(?P<match_id>[0-9]+)$', views.remove_match),
	url(r'jogos/participar/(?P<match_id>[0-9]+)$', views.attend_to_match),
	url(r'jogos/sair/(?P<match_id>[0-9]+)$', views.leave_match),

	url(r'pontuacao/(?P<match_id>[0-9]+)$', views.update_score),
]
