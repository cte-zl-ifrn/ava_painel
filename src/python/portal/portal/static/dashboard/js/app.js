export default {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data() {
        return {
            destaque: null,
            semestres: [],
            situacoes: [
                {"label": "Em andamento", "id": "inprogress"},
                {"label": "Todas as situações", "id": "allincludinghidden"},
                {"label": "Não iniciados", "id": "future"},
                {"label": "Encerrados", "id": "past"},
                {"label": "Favoritos", "id": "favourites"},
            ],
            ordenacoes: [
                {"label": "Ordenado por disciplina", "id": "fullname"},
                {"label": "Ordenado por código do diário", "id": "shortname"},
                {"label": "Ordenado pelo último acessado", "id": "ul.timeaccess desc"},
            ],
            visualizacoes: [
                {"label": "Ver como linhas", "id": "list"},
                {"label": "Ver como cartões", "id": "card"},
            ],
            disciplinas: [],
            cursos: [],
            arquetipos: [],
            ambientes: [],
            coordenacoes: [],
            praticas: [],
            diarios: [],
            salas: [],
        }
    },
    mounted() {
        document.getElementById('grid-filter').classList.remove('hide_this');
        this.filterCards();
    },
    methods: {
        detailme: function(card) {
            this.destaque = card;
        },
        formatDate: function(dateString) {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('default', { dateStyle: 'long' }).format(date);
        },
        favourite: function(card) {
            const new_status = card.isfavourite ? 0 : 1;
            axios.get(
                '/portal/api/v1/set_favourite/', {
                    params: {
                        "ava": card.ambiente.sigla,
                        "courseid": card.id,
                        "favourite": new_status,
                    }
                }
            ).then(response => {
                card.isfavourite = new_status == 1;
            }).catch(error => {
                console.log(error);
            });
        },
        hidden: function(card) {
            const new_status = card.isfavourite ? 0 : 1;
            axios.get(
                '/portal/api/v1/set_hidden/', {
                    params: {
                        "ava": card.ambiente.sigla,
                        "courseid": card.id,
                        "hidden": new_status,
                    }
                }
            ).then(response => {
                card.hidden = new_status == 1;
            }).catch(error => {
                console.log(error);
            });
        },
        filterCards: function(a, b, c) {
            this.filtering()
            axios.get(
                '/portal/api/v1/diarios/', {
                    params: {
                        "semestre": document.getElementById('semestre').value,
                        "situacao": document.getElementById('situacao').value,
                        "ordenacao": document.getElementById('ordenacao').value,
                        "disciplina": document.getElementById('disciplina').value,
                        "curso": document.getElementById('curso').value,
                        "arquetipo": document.getElementById('arquetipo').value,
                        "ambiente": document.getElementById('ambiente_id').value,
                        "q": document.getElementById('q').value,
                        // "page": document.getElementById('page').value,
                        // "page_size": document.getElementById('page_size').value,
                    }
                }
            ).then(response => {
                Object.assign(this, response.data);
                console.log(response.data);
                this.filtered();
            }).then(e => {
                this.filtered();
            });
        },
        changeCourseView: function() {
            var newView = document.getElementById('visualizacao').value;
            var oldView = newView=='list' ? 'cards' : 'list';
            document.getElementById('course-' + newView).classList.remove('hide_this');
            document.getElementById('course-' + oldView).classList.add('hide_this');
        },
        filtering: function() {
            document.getElementById('search-loader').classList.remove('hide_this');
            document.getElementById('course-views').classList.add('hide_this');
        },
        filtered: function() {
            document.getElementById('search-loader').classList.add('hide_this');
            document.getElementById('course-views').classList.remove('hide_this');
        },
    },
}