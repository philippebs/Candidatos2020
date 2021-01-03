from django.urls import path

from . import views

app_name = 'votacao'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:municipio_id>/', views.detail, name='detail'),
    path('<int:municipio_id>/candidato/', views.candidatos, name='candidatos'),
    path('<int:municipio_id>/zona_secao/', views.zonasecao, name='zonasecao'),
    path('<int:municipio_id>/candidato/<int:candidato_id>/<int:ano>/', views.ano_votacao, name='ano_votacao'),
    path('<int:municipio_id>/busca', views.buscar, name='buscar'),
]