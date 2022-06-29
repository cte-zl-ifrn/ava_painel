export default {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data() {
        return {
            destaque: null,
            informativos: [],
            cards: []
        }
    },
    mounted() {
        document.getElementById('app').classList.remove('hide_this');
        axios.get('/portal/api/v1/diarios/').then(response=>{
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