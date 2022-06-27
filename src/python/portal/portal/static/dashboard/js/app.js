export default {
    API_URL: 'https://api.github.com/repos/vuejs/core/commits?per_page=3&sha=',
    data() {
        return {
            message: 'Hello Vue!',
            cards: [
                {
                    "ambiente": {
                        "titulo": "Aberto",
                        "sigla": "A",
                        "classe": "aberto",
                    },
                    "diario": {
                        "titulo": "Diário",
                        "codigo": "asdf",
                        "progresso": 70,
                    }
                },
                {
                    "ambiente": {
                        "titulo": "Aberto",
                        "sigla": "A",
                        "classe": "aberto",
                    },
                    "diario": {
                        "titulo": "Diário 2",
                        "codigo": "asdf",
                        "progresso": 70,
                    }
                },
            ]
        }
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}