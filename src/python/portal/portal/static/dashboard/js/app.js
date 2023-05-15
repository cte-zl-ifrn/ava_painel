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
            ambientes: [],
            coordenacoes: [],
            praticas: [],
            diarios: [],
            salas: [],
            has_error: false,
            is_filtering: true,
            activeParagraph: null,
        }
    },
    mounted() {
        document.getElementById('grid-filter').classList.remove('hide_this');
        this.filterCards();
        
        $(document).ready(function() {
            $('#ambiente_id').select2({
              templateResult: function(data) {
                if (data.element && data.element.dataset) {
                    // window.kkk = data.element.dataset;
                    return $('<span style="border-left: 7px solid ' + data.element.dataset.color + ';padding-left:6px;">' + data.text + '</span> ');
                }
              }
            });
          });
    },
    methods: {
        formatDate: function(dateString) {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('default', { dateStyle: 'long' }).format(date);
        },
        favourite: function(card) {
            const new_status = card.isfavourite ? 0 : 1;
            axios.get(
                '/painel/portal/api/v1/set_favourite/', {
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
        visible: function(card) {
            const new_status = parseInt(card.visible) ? 0 : 1;
            axios.get(
                '/painel/portal/api/v1/set_visible/', {
                    params: {
                        "ava": card.ambiente.sigla,
                        "courseid": card.id,
                        "visible": new_status,
                    }
                }
            ).then(response => {
                card.visible = new_status == 1;
            }).catch(error => {
                console.log(error);
            });
        },
        filterCards: function(a, b, c) {
            this.filtering();
            try {
                axios.get(
                    '/painel/portal/api/v1/diarios/', {
                        params: {
                            "semestre": document.getElementById('semestre').value,
                            "situacao": document.getElementById('situacao').value,
                            "ordenacao": document.getElementById('ordenacao').value,
                            "disciplina": document.getElementById('disciplina').value,
                            "curso": document.getElementById('curso').value,
                            "ambiente": document.getElementById('ambiente_id').value,
                            "q": document.getElementById('q').value,
                        }
                    }
                ).then(response => {
                    Object.assign(this, response.data);
                    this.filtered();
                }).catch(error => {
                    this.has_error = true;
                    this.filtered();
                    return Promise.reject(error)
                });
            } catch (e) {
                console.log(e);
                this.has_error = true;
                this.filtered();
            }
        },
        filtering: function() {
            this.diarios = [];
            this.coordenacoes = [];
            this.praticas = [];
            this.has_error = false;
            this.is_filtering = true;
        },
        filtered: function() {
            this.is_filtering = false;
        },
    },
}
