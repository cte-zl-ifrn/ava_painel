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
                {"label": "Por disciplina", "id": "fullname"},
                {"label": "Por código do diário", "id": "shortname"},
                {"label": "Pelo últimos acessados", "id": "ul.timeaccess desc"},
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
                        // "ambiente": document.getElementById('ambiente').value,
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