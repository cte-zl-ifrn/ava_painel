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
            cards: []
        }
    },
    mounted() {
        document.getElementById('app').classList.remove('hide_this');
        axios.get('/portal/api/v1/diarios/').then(response=>{
            console.log(response.data)
            this.disciplinas = response.data.disciplinas;
            this.status = response.data.status;
            this.competencias = response.data.competencias;
            this.informativos = response.data.informativos;
            this.cards = response.data.cards;
        }).then(function(e) {
            console.log(e);
        });
    },
    methods: {
        detailme: function (card) {
            this.destaque = card;
        }
    },
}