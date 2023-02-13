import logging
from typing import Dict, List, Union, Any
import concurrent
from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from sc4net import get, get_json
from .models import Ambiente, Arquetipo, Situacao, Ordenacao, Visualizacao, Curso
from django.shortcuts import get_object_or_404
import sentry_sdk


def _get_diarios(params: Dict[str, Any]):
    try:
        ambiente = params["ambiente"]
        adict = {
            "ambiente": {
                "titulo": ambiente.nome,
                "sigla": ambiente.sigla,
                "cor": ambiente.cor
            }
        }

        querystrings = [
            f'{k}={v}' if v else "" for k, v in params.items() if k not in ['ambiente', 'results'] and v is not None
        ]

        base_url = ambiente.url if ambiente.url[-1:] != '/' else ambiente.url[:-1]
        url = f'{base_url}/local/suap/api/get_diarios.php?' + \
            "&".join(querystrings)
        result = get_json(url)
        
        for k, v in params['results'].items():
            if k in result:
                if k in ['diarios', 'coordenacoes', 'praticas']:
                    params['results'][k] += [{**diario, **adict} for diario in result[k] or []]
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
