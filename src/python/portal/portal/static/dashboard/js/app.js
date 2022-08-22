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
            console.log(a, b, c);
            axios.get(
                '/portal/api/v1/diarios/', {
                    params: {
                        "disciplina_id": document.getElementById('disciplina_id').value,
                        "status_id": document.getElementById('status_id').value,
                        "competencia_id": document.getElementById('competencia_id').value,
                    }
                }
            ).then(response => {
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
    },
}