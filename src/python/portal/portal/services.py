import logging
import concurrent
import re
from enum import Enum
from typing import Dict, List, Union, Any
from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from sc4net import get, get_json
from .models import Ambiente, Arquetipo, Situacao, Ordenacao, Visualizacao, Curso
from django.shortcuts import get_object_or_404
import sentry_sdk


CODIGO_TURMA_REGEX = re.compile('^(\d\d\d\d\d)\.(\d*)\.(\d*)\.(..)\.(.*)$')
CODIGO_TURMA_ELEMENTS_COUNT = 5
CODIGO_TURMA_SEMESTRE_INDEX = 0
CODIGO_TURMA_PERIODO_INDEX = 1
CODIGO_TURMA_CURSO_INDEX = 2
CODIGO_TURMA_TURMA_INDEX = 3
CODIGO_TURMA_EXCEDENTE_INDEX = 4

CODIGO_DIARIO_REGEX = re.compile('^(\d\d\d\d\d)\.(\d*)\.(\d*)\.(.*)\.(.*\..*)$')
CODIGO_DIARIO_ELEMENTS_COUNT = 5
CODIGO_DIARIO_SEMESTRE_INDEX = 0
CODIGO_DIARIO_PERIODO_INDEX = 1
CODIGO_DIARIO_CURSO_INDEX = 2
CODIGO_DIARIO_TURMA_INDEX = 3
CODIGO_DIARIO_DISCIPLINA_INDEX = 4

CODIGO_COORDENACAO_REGEX = re.compile('^(ZL)\.(\d*)(.*)')
CODIGO_COORDENACAO_ELEMENTS_COUNT = 3
CODIGO_COORDENACAO_CAMPUS_INDEX = 0
CODIGO_COORDENACAO_CURSO_INDEX = 1
CODIGO_COORDENACAO_SUFIXO_INDEX = 2

CODIGO_PRATICA_REGEX = re.compile('^(.*)\.(\d{11,14}\d*)$')
CODIGO_PRATICA_ELEMENTS_COUNT = 2
CODIGO_PRATICA_PREFIXO_INDEX = 0
CODIGO_PRATICA_MATRICULA_INDEX = 1
CODIGO_PRATICA_SUFIXO_INDEX = 2


CURSOS_CACHE = {}


def _merge_curso(diario: dict, codigo_curso: str):
    if codigo_curso not in CURSOS_CACHE and CURSOS_CACHE.get(codigo_curso, None) is None:
        CURSOS_CACHE[codigo_curso] = Curso.objects.filter(codigo=codigo_curso).first()
    curso = CURSOS_CACHE.get(codigo_curso, None)
    if curso is not None:
        diario['curso'] = {'codigo': curso.codigo, 'nome': curso.nome}


def _merge_turma(diario: dict, codigo_turma: tuple):
    if codigo_turma is not None:
        diario['turma'] = '.'.join(codigo_turma[0:CODIGO_TURMA_TURMA_INDEX+1])
        diario['componente'] = codigo_turma[CODIGO_TURMA_EXCEDENTE_INDEX]


def _merge_diario(diario: dict, ambiente: dict):
    codigo = diario['shortname']
    diario_re = CODIGO_DIARIO_REGEX.findall(codigo)
    turma_re = CODIGO_TURMA_REGEX.findall(codigo)
    coordenacao_re = CODIGO_COORDENACAO_REGEX.findall(codigo)
    pratica_re = CODIGO_PRATICA_REGEX.findall(codigo)
    if len(diario_re) > 0 and len(diario_re[0]) == CODIGO_DIARIO_ELEMENTS_COUNT:
        _merge_curso(diario, diario_re[0][CODIGO_DIARIO_CURSO_INDEX])
        _merge_turma(diario, turma_re[0])
    elif len(coordenacao_re) > 0 and len(coordenacao_re[0]) == CODIGO_COORDENACAO_ELEMENTS_COUNT:
        _merge_curso(diario, coordenacao_re[0][CODIGO_COORDENACAO_CURSO_INDEX])
    elif len(pratica_re) > 0 and len(pratica_re[0]) == CODIGO_PRATICA_ELEMENTS_COUNT:
        if len(turma_re) > 0 and len(turma_re[0]) == CODIGO_TURMA_ELEMENTS_COUNT:
            _merge_curso(diario, turma_re[0][CODIGO_TURMA_CURSO_INDEX])
            _merge_turma(diario, turma_re[0])
    return {**diario, **ambiente}


def _get_diarios(params: Dict[str, Any]):
    try:
        ambiente = params["ambiente"]
        ambientedict = {"ambiente": {"titulo": ambiente.nome, "sigla": ambiente.sigla, "cor": ambiente.cor}}

        querystrings = [f'{k}={v}' if v else "" for k, v in params.items() if k not in ['ambiente', 'results'] and v is not None]

        base_url = ambiente.url if ambiente.url[-1:] != '/' else ambiente.url[:-1]
        url = f'{base_url}/local/suap/api/get_diarios.php?' + "&".join(querystrings)
        result = get_json(url)
        
        for k, v in params['results'].items():
            if k in result:
                if k in ['diarios', 'coordenacoes', 'praticas']:
                    params['results'][k] += [_merge_diario(diario, ambientedict) for diario in result[k] or []]
                else:
                    params['results'][k] += result[k] or []
                    
    except Exception as e:
        sentry_sdk.capture_exception(e)


def get_diarios(
    username: str,
    semestre: str = None,
    situacao: str = None,
    ordenacao: str = None,
    disciplina: str = None,
    curso: str = None,
    arquetipo: str = None,
    ambiente: str = None,
    q: str = None,
    page: int = 1,
    page_size: int = 21,
) -> dict:

    results = {
        "semestres": [],
        "ambientes": Ambiente.as_dict(),
        "disciplinas": [],
        "cursos": [],
        "arquetipos": Arquetipo.kv,
        "diarios": [],
        "coordenacoes": [],
        "praticas": [],
    }
    
    has_ambiente = ambiente != '' and ambiente is not None
    
    requests = [
        {
            "ambiente": ava,
            "username": username,
            "semestre": semestre,
            "situacao": situacao,
            "ordenacao": ordenacao,
            "disciplina": disciplina,
            "curso": curso,
            "arquetipo": arquetipo,
            "q": q,
            "page": page,
            "page_size": page_size,
            "results": results,
        } for ava in Ambiente.objects.filter(active=True) if (has_ambiente and int(ambiente) == ava.id) or not has_ambiente
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(_get_diarios, requests)

    results["semestres"] = sorted(results["semestres"], key = lambda e: e['label'], reverse=True)
    results["ambientes"] = sorted(results["ambientes"], key = lambda e: e['label'])
    results["disciplinas"] = sorted(results["disciplinas"], key = lambda e: e['label'])
    results["coordenacoes"] = sorted(results["coordenacoes"], key = lambda e: e['fullname'])
    results["praticas"] = sorted(results["praticas"], key = lambda e: e['fullname'])
    cursos = {c.codigo: c.nome for c in Curso.objects.filter(codigo__in=[x['id'] for x in results["cursos"]])}
    for c in results["cursos"]:
        if c['id'] in cursos:
            c['label'] = f"{cursos[c['id']]} [{c['id']}]"
        else:
            c['label'] = f"Curso [{c['id']}], favor solicitar o cadastro"
            
    results["cursos"] = sorted(results["cursos"], key = lambda e: e['label'])
    results["situacoes"] = Situacao.kv
    results["ordenacoes"] = Ordenacao.kv
    results["visualizacoes"] = Visualizacao.kv

    return results


def get_atualizacoes_counts(username: str) -> dict:
    def _callback(params):
        try:
            ava = params["ava"]

            counts = get_json(f'{ava.base_api_url}/get_atualizacoes_counts.php?username={params["username"]}')
            counts["ambiente"] = {
                "titulo": ava.nome, 
                "sigla": ava.sigla, 
                "cor": ava.cor, 
                "notifications_url": f"{ava.base_url}/message/output/popup/notifications.php",
                "conversations_url": f"{ava.base_url}/message/",
            }
            params['results']["atualizacoes"].append(counts)
            params['results']["unread_notification_total"] = sum([c['unread_popup_notification_count'] for c in params['results']["atualizacoes"]])
            params['results']["unread_conversations_total"] = sum([c['unread_conversations_count'] for c in params['results']["atualizacoes"]])
            
        except Exception as e:
            logging.error(e)
            sentry_sdk.capture_exception(e)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = {"atualizacoes": [], "unread_notification_total": 0, "unread_conversations_total": 0}
        requests = [{"username": username, "ava": ava,"results": results,} for ava in Ambiente.objects.filter(active=True)]
        executor.map(_callback, requests)

    results["atualizacoes"] = sorted(results["atualizacoes"], key = lambda e: e['ambiente']['titulo'])
    return results


    return [
        {
            "error": False,
            "data": {
                "conversations": [{"id": 107, "name": "", "subname": None, "imageurl": None, "type": 1, "membercount": 2, "ismuted": False, "isfavourite": False, "isread": False, "unreadcount": 1, "members": [{"id": 5, "fullname": "Kelson da Costa Medeiros", "profileurl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/user\/profile.php?id=5", "profileimageurl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f1?rev=457", "profileimageurlsmall": "https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f2?rev=457", "isonline": True, "showonlinestatus": True, "isblocked": False, "iscontact": False, "isdeleted": False, "canmessageevenifblocked": True, "canmessage": False, "requirescontact": False, "contactrequests": []}], "messages":[{"id": 1, "useridfrom": 5, "text": "<p>teste<\/p>", "timecreated": 1669392466}], "candeletemessagesforallusers": False}]
            }
        }
    ]


def set_favourite_course(username: str, ava: str, courseid: int, favourite: int) -> dict:
    ava = get_object_or_404(Ambiente, sigla=ava)
    return get_json(f'{ava.base_api_url}/set_favourite_course.php?username={username}&courseid={courseid}&favourite={favourite}')


def set_hidden_course(username: str, ava: str, courseid: int, hidden: int) -> dict:
    ava = get_object_or_404(Ambiente, sigla=ava)
    return get_json(f'{ava.base_api_url}/set_hidden_course.php?username={username}&courseid={courseid}&hidden={hidden}')
