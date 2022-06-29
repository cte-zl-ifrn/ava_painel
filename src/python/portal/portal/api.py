from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)

@api.get("/diarios/")
def diarios(request):
    return {
            "informativos": [
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
            ],
            "cards": [
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0341", "progresso": 10, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com", "eventos": []}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0342", "progresso": 20, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 30, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 70, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 70, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 70, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 70, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
                {
                    "ambiente": { "titulo": "Aberto", "sigla": "A", "classe": "aberto", },
                    "diario": { "titulo": "DESENVOLVIMENTO DE PROJETOS COM O USO DE TECNOLOGIAS DIGITAIS", "codigo": "2020.1.15046.1E.POS.0345", "progresso": 70, "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=287&q=80", "url": "https://google.com"}
                },
            ]
        }