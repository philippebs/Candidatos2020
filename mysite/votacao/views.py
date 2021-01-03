from django.shortcuts import get_object_or_404 , render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.db.models import Sum

from .models import Municipio, MunicipioZona, Candidato, CandidatoPartido, Partido, TipoCandidato, Voto

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

import asyncio
from asgiref.sync import sync_to_async

# Create your views here.
def index(request):
    municipio_list = Municipio.objects.all()
    context = {'municipio_list': municipio_list}
    return render(request, 'votacao/index.html', context)


def detail(request, municipio_id):
    municipio = get_object_or_404(Municipio, pk=municipio_id)
    return render(request, 'votacao/detail.html', {'municipio': municipio})


def candidatos(request, municipio_id):
    municipio = get_object_or_404(Municipio, pk=municipio_id)
    candidato_partido_list = CandidatoPartido.objects.filter(municipio_id=municipio_id)
    context = {'candidato_partido_list': candidato_partido_list, 'municipio': municipio}
    return render(request, 'votacao/candidatos.html', context)


def zonasecao(request, municipio_id):
    municipio = get_object_or_404(Municipio, pk=municipio_id)
    municipio_zona_list = MunicipioZona.objects.filter(municipio_id=municipio_id)
    context = {'municipio_zona_list': municipio_zona_list, 'municipio': municipio}
    return render(request, 'votacao/zonasecao.html', context)

def ano_votacao(request, municipio_id, candidato_id, ano):
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    votos = Voto.objects.filter(candidato_partido__candidato_id=candidato_id, municipio_zona__municipio_id=municipio_id, candidato_partido__ano=ano)
    total = votos.aggregate(Sum('quantidade'))['quantidade__sum']
    context = {'votos': votos, 'candidato': candidato, 'total': total}
    return render(request, 'votacao/votos.html', context)


def buscar(request, municipio_id):
    ano = 2020
    municipio = get_object_or_404(Municipio, pk=municipio_id)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    chrome = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    municipio_zona_list = MunicipioZona.objects.filter(municipio_id=municipio_id)
    total = len(municipio_zona_list)
    atual = 0
    tipo_candidato_list = TipoCandidato.objects.all()
    partido_list = Partido.objects.all()
    candidato_list = Candidato.objects.all()
    candidato_partido_list = CandidatoPartido.objects.filter(ano=ano, municipio_id=municipio_id)
    voto_list = Voto.objects.filter(municipio_zona__municipio_id=municipio_id, candidato_partido__ano=ano)
    atual = 0
    for municipio_zona in municipio_zona_list:
        atual = atual + 1
        percentual = ((atual * 100) / total)
        site = 'https://resultados.tse.jus.br/oficial/#/divulga-desktop/boletins-de-urna;e=426;uf=rj;zonaBU=%s;secaoBU=%s;municipioBU=%s' % (municipio_zona.zona, municipio_zona.secao, municipio_zona.municipio.numero)
        chrome.get(site)
        time.sleep(1)
        html = chrome.page_source
        soup = BeautifulSoup(html, "html.parser")
        sections = soup.find_all('app-lista-candidatos-bu')
        for section in sections:
            section_candidatos = section.find_all('div', attrs={'class' : 'odd-in-scss flex items-center justify-between py-2 px-4 text-gray-600 tracking-tighter'})
            for div in section_candidatos:
                nome_div = div.find_all('div', attrs={'class' : 'text-lg font-bold'})[0].text.strip()
                numero_candidato = ''.join(nome_div.split(' - ')[0])
                nome_candidato = ''.join(nome_div.split(' - ')[1])

                partido_nome = div.find_all('div', attrs={'class' : 'text-xs font-semibold'})[0].text.strip()
                votos = div.find_all('div', attrs={'class' : 'text-ion-tertiary text-lg font-bold'})[0].text.strip()
                
                candidato = next((item for item in candidato_list if item.nome == nome_candidato), None)
                if not candidato:
                    candidato = Candidato(nome=nome_candidato)
                    candidato.save()
                    candidato_list = Candidato.objects.all()

                #Fazendo a busca pelo partido correto na lista, e salva se não existe
                numero_partido = int(str(numero_candidato)[0:2])
                partido = next((partido for partido in partido_list if partido.numero == numero_partido), None)
                if not partido:
                    partido = Partido(nome=partido_nome, numero=numero_partido)
                    partido.save()
                    partido_list = Partido.objects.all()

                tipo_candidato=None 
                if len(numero_candidato) == 2:
                    tipo_candidato = next((tipo for tipo in tipo_candidato_list if tipo.nome == 'Prefeito'), None)
                else:
                    tipo_candidato = next((tipo for tipo in tipo_candidato_list if tipo.nome == 'Vereador'), None)

                candidato_partido = next((item for item in candidato_partido_list if item.candidato.nome == candidato.nome), None)
                if not candidato_partido:
                    candidato_partido = CandidatoPartido(nome=nome_candidato, numero=numero_candidato, municipio=municipio_zona.municipio, ano=ano, candidato=candidato, partido=partido, tipo_candidato=tipo_candidato)
                    candidato_partido.save()
                    candidato_partido_list = CandidatoPartido.objects.filter(ano=ano, municipio_id=municipio_id)

                voto = next((item for item in voto_list if item.candidato_partido.id == candidato_partido.id and item.municipio_zona.zona == municipio_zona.zona and item.municipio_zona.secao == municipio_zona.secao), None)
                if not voto:
                    voto = Voto(candidato_partido=candidato_partido, municipio_zona=municipio_zona, quantidade=int(votos),turno=1)
                    voto.save()
        print('Carregando: %s%%' % (round(percentual, 2)), end='\r')
                

    # votos = Voto.objects.filter(candidato_partido__candidato_id=candidato_id, municipio_zona__municipio_id=municipio_id, candidato_partido__ano=ano)
    # context = {'votos': votos, 'candidato': candidato}
    return redirect('votacao:detail', municipio_id = municipio_id)