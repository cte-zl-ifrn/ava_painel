from typing import Dict, List, Union, Any
import concurrent
from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from sc4net import get, get_json
from .models import Ambiente


def get_disciplinas(username: str) -> List[Dict[str, Union[str, int]]]:
    return get_json('http://ava01:80/local/suapsync/api/get_disciplinas.php?username=2080882')


def get_situacoes() -> Dict[str, str]:
    return [
        {"id": "all", "label": "Todos"},
        {"id": "inprogress", "label": "Em andamento"},
        {"id": "future", "label": "Não iniciados"},
        {"id": "past", "label": "Encerrados"},
        {"id": "favourites", "label": "Meus favoritos"},
        {"id": "hidden", "label": "Ocultados"},
    ]


def get_semestres(username: str) -> dict:
    return [
        {"id": "20201", "label": "2020.1"},
        {"id": "20202", "label": "2020.2"},
        {"id": "20222", "label": "2022.2"},
    ]

def _get_diarios(params: Dict[str, Any]):
    try:
        ambiente_dict = {"titulo": params["ambiente"].nome, "sigla": params["ambiente"].sigla, "classe": "ambiente01", }
        base_url = params["ambiente"].url if params["ambiente"].url[-1:] != '/' else params["ambiente"].url[:-1]
        url = f'{base_url}/local/suapsync/api/get_diarios.php?username={params["username"]}&student={params["as_student"]}'
        url += f"&disciplina={params['disciplina']}" if params['disciplina'] else ""
        url += f"&situacao={params['situacao']}" if params['situacao'] else ""
        url += f"&semestre={params['semestre']}" if params['semestre'] else ""
        url += f"&q={params['q']}" if params['q'] else ""
        print(url)
        result = get_json(url)
        print(result)
        params['results']["disciplinas"] += result.get("disciplinas", [])
        params['results']["competencias"] += result.get("semestres", [])
        params['results']["cards"] += [ {"ambiente": ambiente_dict, "diario": diario } for diario in result.get("diarios", [])]
    except Exception as e:
        print("error", e)
    

def get_diarios(as_student: int, username: str, disciplina: str = None, situacao: str = None, semestre: str = None, q: str = None) -> dict:
    results = {
        "disciplinas": [],
        "statuses": [
            {'id': 'allincludinghidden', 'label': 'Sem filtro'},
            {'id': 'inprogress', 'label': 'Em andamento'},
            {'id': 'future', 'label': 'Não iniciados'},
            {'id': 'past', 'label': 'Encerrados'},
            {'id': 'favourites', 'label': 'Favoritos'},
        ],
        "competencias": [],
        "cards": [],
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        print([ambiente.url for ambiente in Ambiente.objects.filter(active=True)])
        executor.map(_get_diarios, [{
            "ambiente": ambiente,
            "results": results,
            "username": username,
            "disciplina": disciplina,
            "situacao": situacao,
            "semestre": semestre,
            "as_student": as_student,
            "q": q,
            } for ambiente in Ambiente.objects.filter(active=True)])
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
    return [{
        "error": False,
        "data": {
            "notifications": [{
                "id": 254,
                "useridfrom": -20,
                "useridto": 5,
                "subject": "Estudantes com risco em L\u00f3gica e Algoritmos cursos","shortenedsubject":"Estudantes com risco em L\u00f3gica e Algoritmos cursos",
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
            }],
            "unreadcount": 1
        }
    }]


def get_mensagens(username: str) -> dict:
    return [{"error":False,"data":{"conversations":[{"id":107,"name":"","subname":None,"imageurl":None,"type":1,"membercount":2,"ismuted":False,"isfavourite":False,"isread":False,"unreadcount":1,"members":[{"id":5,"fullname":"Kelson da Costa Medeiros","profileurl":"https:\/\/teste.ava.ifrn.edu.br\/gui\/user\/profile.php?id=5","profileimageurl":"https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f1?rev=457","profileimageurlsmall":"https:\/\/teste.ava.ifrn.edu.br\/gui\/pluginfile.php\/22\/user\/icon\/moove\/f2?rev=457","isonline":True,"showonlinestatus":True,"isblocked":False,"iscontact":False,"isdeleted":False,"canmessageevenifblocked":True,"canmessage":False,"requirescontact":False,"contactrequests":[]}],"messages":[{"id":1,"useridfrom":5,"text":"<p>teste<\/p>","timecreated":1669392466}],"candeletemessagesforallusers":False}]}}]
