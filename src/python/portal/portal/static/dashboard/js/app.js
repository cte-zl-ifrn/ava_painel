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
            const new_status = card.hidden ? 0 : 1;
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
            this.filtering();
            try {
                axios.get(
                    '/portal/api/v1/diarios/', {
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
        isActive(id){
            return this.activeParagraph === id;
        },
        addActiveClass(id){
            this.activeParagraph = id;
        },
    },
}






// var maisDetalhes = document.getElementsByClassName("mais-detalhes-card");
// var lessHr = document.getElementsByClassName("menos-detalhes-hr");
// var lessDetails = document.getElementsByClassName("menos-detalhes-card");


// maisDetalhes[0].addEventListener('click', function() {
//    alert("teste");
//     maisDetalhes.classList.add("d-none");
// });

// lessDetails[0].addEventListener('click', function() {
//     lessDetails.classList.remove("d-none");
//     lessHr.classList.remove("d-none");
// });

// $("#mais-detalhes-card").click(function() {
//     alert("teste");
//     $("#mais-detalhes-card").addClass("d-none");

//     $("#menos-detalhes-hr").removeClass("d-none");
//     $("#menos-detalhes-card").removeClass("d-none");
// });

// $("#menos-detalhes-card").click(function() {
//     $("#mais-detalhes-card").removeClass("d-none");

//     $("#menos-detalhes-card").addClass("d-none");
//     $("#menos-detalhes-hr").addClass("d-none");
// });


