from typing import Dict, List, Union, Any
import concurrent
from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from sc4net import get, get_json
from .models import Ambiente, Arquetipo, Situacao, Ordenacao, Visualizacao, Curso


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
        
        print(result)

        for k, v in params['results'].items():
            if k in result:
                if k in ['diarios', 'coordenacoes', 'praticas']:
                    params['results'][k] += [{**diario, **adict} for diario in result[k] or []]
                else:
                    params['results'][k] += result[k] or []
                    
    except Exception as e:
        print("error", e)


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
    }

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
        } for ava in Ambiente.objects.filter(active=True) if ambiente == ava.id or ambiente != '' or ambiente is not None
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(_get_diarios, requests)


    results["semestres"] = sorted(results["semestres"], key = lambda e: e['label'], reverse=True)
    results["ambientes"] = sorted(results["ambientes"], key = lambda e: e['label'])
    results["disciplinas"] = sorted(results["disciplinas"], key = lambda e: e['label'])
    results["coordenacoes"] = sorted(results["coordenacoes"], key = lambda e: e['fullname'])
    cursos = {c.codigo: c.nome for c in Curso.objects.filter(codigo__in=[x['id'] for x in results["cursos"]])}
    for c in results["cursos"]:
        if c['id'] in cursos:
            c['label'] = f"{cursos[c['id']]} [{c['id']}]"
    results["cursos"] = sorted(results["cursos"], key = lambda e: e['label'])
    results["situacoes"] = Situacao.kv
    results["ordenacoes"] = Ordenacao.kv
    results["visualizacoes"] = Visualizacao.kv

    return results


def get_informativos(username: str) -> dict:
    return [
        {
            "titulo": "PLAFOREDU – MEC lança plataforma virtual com 280 cursos de capacitação gratuitos. Clique aqui e saiba como estudar",
            "url": "https://ead.ifrn.edu.br/portal/mec-lanca-plataforma-virtual-com-280-cursos-de-capacitacao-gratuitos/",
            "noticia": "Reportagem: Laurence Campos O Ministério da Educação (MEC) lançou este mês a plataforma PlaforEDU, um ambiente virtual de aprendizado para formação continuada de servidores da Rede Federal de Ensino de Educação Básica, Técnica e Tecnológica. Na plataforma, os professores terão à disposição 280 cursos gratuitos de capacitação. As aulas são divididas em 05 trilhas do"
        },
        {
            "titulo": "SEMEAD 2022 – Últimos dias para a submissão de trabalhos. Clique aqui e saiba como se inscrever",
            "url": "https://ead.ifrn.edu.br/portal/semead-2022-ultimos-dias-para-a-submissao-de-trabalhos-clique-aqui-e-saiba-como-se-inscrever/",
            "noticia": "Quase tudo pronto para a quinta edição do Seminário Internacional de Educação a Distância! O evento, cuja programação inclui palestras, conferências, minicursos, mesas redondas e apresentação de trabalhos, irá acontecer de forma online nos dias 18, 19 e 20 de maio de 2022."
        },
    ]


def get_notificacoes(username: str) -> dict:
    return [
        {
            "error": False,
            "data":
            {
                "unreadcount": 1,
                "ambientes":
                [
                    {
                        "titulo": "Acadêmico",
                        "sigla": "ZL",
                        "cor": "#438f4b",
                        "unreadcount": 1,
                        "notifications":
                        [
                            {
                                "id": 254,
                                "useridfrom": -20,
                                "useridto": 5,
                                "subject": "Estudantes com risco em L\u00f3gica e Algoritmos cursos", "shortenedsubject": "Estudantes com risco em L\u00f3gica e Algoritmos cursos",
                                "text": "<p>Ol\u00e1, Kelson,<br>\n&lt;p&gt;Alguns estudantes inscritos em L\u00f3gica e Algoritmos n\u00e3o acessaram o curso recentemente.&lt;\/p&gt;<br>\n<br>\nhttps:\/\/teste.ava.ifrn.edu.br\/gui\/report\/insights\/insights.php?modelid=5&amp;contextid=56<\/p>",
                                "fullmessage": "Ol\u00e1, Kelson,\n<p>Alguns estudantes inscritos em L\u00f3gica e Algoritmos n\u00e3o acessaram o curso recentemente.<\/p>\n\nhttps:\/\/teste.ava.ifrn.edu.br\/gui\/report\/insights\/insights.php?modelid=5&contextid=56",
                                "fullmessageformat": 2,
                                "fullmessagehtml": "<head><style>\nbody:not(.dir-ltr):not(.dir-rtl) {\n    font-family: 'Open Sans', sans-serif;\n}\n.btn-insight {\n    color: #007bff;\n    background-color: transparent;\n    display: inline-block;\n    font-weight: 400;\n    text-align: center;\n    white-space: nowrap;\n    vertical-align: middle;\n    user-select: none;\n    border: 1px solid #007bff;\n    padding: .375rem .75rem;\n    line-height: 1.5;\n    border-radius: 0;\n    text-decoration: none;\n    cursor: pointer;\n}\n<\/style><\/head>\n\nOl\u00e1, Kelson,\n<p>Alguns estudantes inscritos em L\u00f3gica e Algoritmos n\u00e3o acessaram o curso recentemente.<\/p>\n<br\/><br\/>\n<a class=\"btn btn-outline-primary btn-insight\" href=\"https:\/\/teste.ava.ifrn.edu.br\/gui\/report\/insights\/insights.php?modelid=5&amp;contextid=56\">Ver insight<\/a>",
                                "smallmessage": "Ol\u00e1, Kelson,\n<p>Alguns estudantes inscritos em L\u00f3gica e Algoritmos n\u00e3o acessaram o curso recentemente.<\/p>\n\nhttps:\/\/teste.ava.ifrn.edu.br\/gui\/report\/insights\/insights.php?modelid=5&contextid=56",
                                "contexturl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/report\/insights\/insights.php?modelid=5&contextid=56",
                                "contexturlname": "Estudantes com risco em L\u00f3gica e Algoritmos cursos",
                                "timecreated": 1667743203,
                                "timecreatedpretty": "19 dias 2 horas atr\u00e1s",
                                "timeread": None,
                                "read": False,
                                "deleted": False,
                                "iconurl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/theme\/image.php\/moove\/core\/1665688157\/i\/marker",
                                "component": "moodle",
                                "eventtype": "insights",
                                "customdata": None
                            }
                        ]
                    }
                ]
            }
        }
    ]


def get_mensagens(username: str) -> dict:
    return [
        {
            "error": False,
            "data": {
                "conversations": [{"id": 107, "name": "", "subname": None, "imageurl": None, "type": 1, "membercount": 2, "ismuted": False, "isfavourite": False, "isread": False, "unreadcount": 1, "members": [{"id": 5, "fullname": "Kelson da Costa Medeiros", "profileurl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/user\/profile.php?id=5", "profileimageurl": "https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f1?rev=457", "profileimageurlsmall": "https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f2?rev=457", "isonline": True, "showonlinestatus": True, "isblocked": False, "iscontact": False, "isdeleted": False, "canmessageevenifblocked": True, "canmessage": False, "requirescontact": False, "contactrequests": []}], "messages":[{"id": 1, "useridfrom": 5, "text": "<p>teste<\/p>", "timecreated": 1669392466}], "candeletemessagesforallusers": False}]
            }
        }
    ]
