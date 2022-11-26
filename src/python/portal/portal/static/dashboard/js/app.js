export default {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data() {
        return {
            destaque: null,
            disciplinas: [],
            status: [],
            competencias: [],
            informativos: [],
            cards: [],
        }
    },
    mounted() {
        axios.get('/portal/api/v1/diarios/').then(response => {
            console.log(response.data);
            this.disciplinas = response.data.disciplinas;
            this.statuses = response.data.statuses;
            this.competencias = response.data.competencias;
            this.informativos = response.data.informativos;
            this.cards = response.data.cards;
            document.getElementById('app').classList.remove('hide_this');
        }).then(e => {
            console.log(e);
        });
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
            axios.get(
                '/portal/api/v1/diarios/', {
                    params: {
                        "student": 1,
                        "disciplina": document.getElementById('disciplina_id').value,
                        "situacao": document.getElementById('status_id').value,
                        "semestre": document.getElementById('competencia_id').value,
                    }
                }
            ).then(response => {
                this.disciplinas = response.data.disciplinas;
                this.statuses = response.data.statuses;
                this.competencias = response.data.competencias;
                this.informativos = response.data.informativos;
                this.cards = response.data.cards;
                document.getElementById('app').classList.remove('hide_this');
            }).then(e => {
                console.log(e);
            });
        },
    },
}