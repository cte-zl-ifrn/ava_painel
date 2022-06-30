from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

api = NinjaAPI(docs_decorator=staff_member_required)

@api.get("/diarios/")
def diarios(request):
    def competencia(codigo):
        return codigo[0:4] + '.' + codigo[4:5]
    agora = datetime.now()
    amanha = agora
    proximo_mes =  agora
    mock_eventos = [
                        {"titulo": "Prova presencial #1", "data_hora_inicio": agora, "data_hora_fim": agora.isoformat(),},
                        {"titulo": "Prova presencial #1", "data_hora_inicio": amanha.isoformat(), "data_hora_fim": amanha.isoformat(),},
                        {"titulo": "Prova presencial #1", "data_hora_inicio": proximo_mes.isoformat(), "data_hora_fim": proximo_mes.isoformat(),},
                    ]
    mock_diarios_all = [
                {
                    "ambiente": { "titulo": "Projetos", "sigla": "Proj", "classe": "ambiente01", },
                    "diario": { 
                        "titulo": "Planilhas eletrônicas para administradores de recursos humanos e gestores de pessoas", 
                        "codigo": "20201.1.15046.1E.FIC.0001", 
                        "progresso": 10,
                        "thumbnail": "https://th.bing.com/th/id/R.0237469cd14e1cd0f36df81e72e84e46?rik=EO9TkycCFK9HGg&riu=http%3a%2f%2fintranetsc.net%2fweb%2fimage%2f2561%2fbackground_excel.jpg&ehk=DDtRX9wkC1POth%2bPCacQZUrGXLBNu1Dr3XB9eJQvuYw%3d&risl=&pid=ImgRaw&r=0", 
                        "url": "https://www.microsoft.com/pt-br/microsoft-365/p/excel/CFQ7TTC0HR4R?ef_id=4c1eeb541f9b1613d04689e9d74cc403:G:s&OCID=AIDcmm409lj8ne_SEM_4c1eeb541f9b1613d04689e9d74cc403:G:s&lnkd=Bing_O365SMB_Brand&msclkid=4c1eeb541f9b1613d04689e9d74cc403", 
                        "eventos": mock_eventos
                    }
                },
                {
                    "ambiente": { "titulo": "Projetos", "sigla": "Proj", "classe": "ambiente01", },
                    "diario": { 
                        "titulo": "Processadores de texto para administradores de recursos humanos e gestores de pessoas", 
                        "codigo": "20201.1.15046.1E.FIC.0002", 
                        "progresso": 20,
                        "thumbnail": "https://th.bing.com/th/id/OIP.pE80XDyNWKyIVdTyzmwBZQHaDt?pid=ImgDet&rs=1", 
                        "eventos": mock_eventos
                    }
                },
                {
                    "ambiente": { "titulo": "Projetos", "sigla": "Proj", "classe": "ambiente01", },
                    "diario": { 
                        "titulo": "10 dicas para melhor sua dissertação", 
                        "codigo": "20201.1.15045.1E.FIC.0003", 
                        "progresso": 30,
                        "thumbnail": "https://blogdoenem.com.br/wp-content/uploads/2019/02/Reda%C3%A7%C3%A3o-par%C3%A1grafos-d.jpg", 
                        "url": "https://google.com", 
                    }
                },
                {
                    "ambiente": { "titulo": "Acadêmico", "sigla": "ZL", "classe": "ambiente02", },
                    "diario": { 
                        "titulo": "Lingua portuguesa aplicada à computação", 
                        "codigo": "20202.1.15047.2E.POS.0003", 
                        "progresso": 30,
                        "thumbnail": "https://blogdoenem.com.br/wp-content/uploads/2019/02/Reda%C3%A7%C3%A3o-par%C3%A1grafos-d.jpg", 
                        "url": "https://google.com", 
                    }
                },
                {
                    "ambiente": { "titulo": "Acadêmico", "sigla": "ZL", "classe": "ambiente02", },
                    "diario": { 
                        "titulo": "Matemática aplicada à computação", 
                        "codigo": "20202.1.15047.2E.POS.0003", 
                        "progresso": 100,
                        "thumbnail": "https://th.bing.com/th/id/OIP.dYcwBTLQt_hgMfZB1dH30AHaFL?pid=ImgDet&rs=1", 
                        "url": "https://google.com", 
                    }
                },
                {
                    "ambiente": { "titulo": "Presencial", "sigla": "P", "classe": "ambiente03", },
                    "diario": { 
                        "titulo": "Banco de dados 1", 
                        "codigo": "20202.1.15047.1E.POS.0003", 
                        "progresso": 30,
                        "thumbnail": "https://th.bing.com/th/id/OIP.M782f_cLfob7BYLEoe_T1wHaEK?pid=ImgDet&rs=1", 
                        "url": "https://google.com", 
                    }
                },
                {
                    "ambiente": { "titulo": "Presencial", "sigla": "P", "classe": "ambiente03", },
                    "diario": { 
                        "titulo": "Lógica de programação", 
                        "codigo": "20202.1.15047.1E.POS.0003", 
                        "progresso": 30,
                        "thumbnail": "https://i.ytimg.com/vi/QACnZP4fhE4/maxresdefault.jpg", 
                        "url": "https://google.com", 
                    }
                },
                {
                    "ambiente": { "titulo": "Presencial", "sigla": "P", "classe": "progress-bar ambiente03", },
                    "diario": { 
                        "titulo": "Lógica de programação", 
                        "codigo": "20202.1.15047.1E.POS.0003", 
                        "progresso": 30,
                        "thumbnail": "https://codigital.ec/wp-content/uploads/2020/10/aprender_python.jpg", 
                        "url": "https://google.com", 
                    }
                },
            ]
    print(request.GET)
    if 'competencia_id' in request.GET:
        mock_diarios = [x for x in mock_diarios_all if competencia(x['diario']['codigo']) == request.GET['competencia_id']]
    else:
        mock_diarios = mock_diarios_all
    mock_informativos = [
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
    mock_disciplinas = [{"label": d['diario']['titulo'], "id": d['diario']['codigo'][-8:]} for d in mock_diarios_all]
    mock_statuses = [
        {"label": "Todos", "id": None},
        {"label": "Em andamento", "id": 1},
        {"label": "Concluídos", "id": 2},
        {"label": "Previstos", "id": 3},
        {"label": "ocultos", "id": 4},
    ]
    mock_competencias = [{"label": d, "id": d} for d in set([competencia(x['diario']['codigo']) for x in mock_diarios_all])]
    
    return {
            "disciplinas": mock_disciplinas,
            "statuses": mock_statuses,
            "competencias": mock_competencias,
            "informativos": mock_informativos,
            "cards": mock_diarios
        }