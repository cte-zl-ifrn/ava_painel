export default {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data() {
        return {
            destaque: null,
            semestres: [],
            situacoes: [
                { "label": "✳️ Diários em andamento", "id": "inprogress" },
                { "label": "🗓️ Diários a iniciar", "id": "future" },
                { "label": "📕 Encerrados pelo professor", "id": "past" },
                { "label": "⭐ Meus diários favoritos", "id": "favourites" },
                { "label": "♾️ Todos os diários (lento)", "id": "allincludinghidden" },
            ],
            ordenacoes: [
                { "label": "📗 Ordenado por nome da disciplina", "id": "fullname" },
                { "label": "🔢 Ordenado por código do diário", "id": "shortname" },
                // { "label": "🕓 Ordenado pelo último acessado", "id": "ul.timeaccess desc" },
            ],
            visualizacoes: [
                { "label": "Ver como linhas", "id": "list" },
                { "label": "Ver como cartões", "id": "card" },
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
            filter_q: localStorage.filter_q,
            filter_situacao: localStorage.filter_situacao || 'inprogress',
            filter_ordenacao: localStorage.filter_ordenacao || 'fullname',
            filter_semestre: localStorage.filter_semestre || '',
            filter_disciplina: localStorage.filter_disciplina != undefined && localStorage.filter_disciplina != null ? localStorage.filter_disciplina : '',
            filter_curso: localStorage.filter_curso || '',
            filter_ambiente: localStorage.filter_ambiente || '',
        }
    },

    mounted() {
        $('.view-toggler').change(this.viewToggle);
        $(document).ready(this.customizeAmbiente);
        this.restoreState();
        this.filterCards();
        this.startTour001();
    },
    methods: {
        restoreState() {
            document.getElementById('grid-filter').classList.remove('hide_this');
            if (!$(".view-toggler").is(":checked")) {
                const lastView = localStorage.view_toggler ? localStorage.view_toggler : 'default';
                $('#toggler-' + lastView).prop('checked', true)
            }
        },

        saveState() {
            localStorage.filter_q = $("#q").val();
            localStorage.filter_situacao = $("#situacao").val();
            localStorage.filter_ordenacao = $("#ordenacao").val();
            localStorage.filter_semestre = $("#semestre").val() || '';
            localStorage.filter_disciplina = $("#disciplina").val() || '';
            localStorage.filter_curso = $("#curso").val() || '';
            localStorage.filter_ambiente = $("#ambiente").val() || '';
        },

        viewToggle() {
            localStorage.view_toggler = $(".view-toggler:checked").val();
            $('.courses').removeClass("default compact").addClass(localStorage.view_toggler);
        },

        customizeAmbiente() {
            /* 
            $('#ambiente').select2({
                templateResult: function (data) {
                    const style = data.element && data.element.dataset && data.element.dataset.color ?
                        ' style="border-left: 10px solid ' + data.element.dataset.color + '; padding: 0 4px;"' : ' class="todos_ambientes"';
                    return $('<span ' + style + '>' + data.text + '</span> ');
                },
                templateSelection: function (data) {
                    const style = data.element && data.element.dataset && data.element.dataset.color ?
                        ' style="border-left: 10px solid ' + data.element.dataset.color + '; padding: 0 4px;"' : ' class="todos_ambientes"';
                    return $('<span ' + style + '>' + data.text + '</span> ');
                }
            });
            $('#ambiente').on("select2:select", this.filterCards);
            $('#ambiente').val(self.filter_ambiente || ''); 
            */
        },

        startTour001() {
            const geral = this;
            if (localStorage.getItem("completouTour001") != 'true') {
                // https://github.com/votch18/webtour.js
                // A ser analisado: https://shepherdjs.dev/
                // Descartei: https://jrainlau.github.io/smartour/
                // Descartei: https://codyhouse.co/demo/product-tour/index.html
                // Não considerei: https://jsfiddle.net/eugenetrue/q465gb7L/
                // Não considerei: https://tooltip-sequence.netlify.app/
                // Descartei pois é pago: https://introjs.com/
                const wt = new WebTour();
                wt.setSteps([
                    {
                        element: '#dropdownMenuSuporte',
                        title: 'Precisa de ajuda?',
                        content: 'Aqui você tem um lista de canais para lhe ajudarmos.',
                        placement: 'bottom-end',
                    },
                    {
                        element: '#all-notifications',
                        title: 'Avisos',
                        content: 'Aqui você verá quantas <strong>notificações</strong> e <strong>mensagens</strong> existem em cada AVA.',
                        placement: 'bottom-end',
                    },
                    {
                        element: '.header-user',
                        title: 'Menu usuário',
                        content: 'Acesse seu perfil no SUAP ou saia do Painel AVA de forma segura.',
                        placement: 'bottom-end',
                    },
                    {
                        element: '#grid-filter-wrapper',
                        title: 'Filtros',
                        content: '<p>Aqui você pode filtrar diários por semestre, curso, turma, disciplina, código/id do diário, curso, ambiente (AVA) ou situação, além de poder ordenar como será visto.</p><p>Você pode começar digitando o nome da disciplina e precionando [ENTER] como uma primeira procura.</p>',
                        placement: 'bottom',
                        onNext: function () {
                            $('#toggler-default').prop('checked', true);
                            geral.viewToggle();
                        }
                    },
                    {
                        element: '#toggler-default-label',
                        title: 'Visão padrão',
                        content: '<p>Aqui você poderá ver os dados dos diários na visão padrão.</p>',
                        placement: 'left-end',
                        onNext: function () {
                            $('#toggler-compact').prop('checked', true);
                            geral.viewToggle();
                        }
                    },
                    {
                        element: '#toggler-compact-label',
                        title: 'Visão compacta',
                        content: '<p>Se você precisar também é possível ter uma visão compacta para listar mais diários de uma só vez na tela.</p>',
                        placement: 'left-end',
                        onNext: function () {
                            $('#toggler-default').prop('checked', true);
                            geral.viewToggle();
                        }
                    },
                ]);
                wt.start();
                localStorage.setItem("completouTour001", true);
            }
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('default', { dateStyle: 'long' }).format(date);
        },

        favourite(card) {
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
                console.debug(error);
            });
        },

        visible(card) {
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
                console.debug(error);
            });
        },

        filterCards() {
            this.filtering();
            this.saveState();
            try {
                axios.get(
                    '/painel/portal/api/v1/diarios/', {
                    params: {
                        "situacao": $('#situacao').val(),
                        "ordenacao": $('#ordenacao').val(),
                        "semestre": $('#semestre').val(),
                        "disciplina": $('#disciplina').val(),
                        "curso": $('#curso').val(),
                        "ambiente": $('#ambiente').val(),
                        "q": $('#q').val(),
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
                console.debug(e);
                this.has_error = true;
                this.filtered();
            }
        },


        filtering() {
            this.diarios = [];
            this.coordenacoes = [];
            this.praticas = [];
            this.has_error = false;
            this.is_filtering = true;
        },


        filtered() {
            this.viewToggle();
            this.restoreState();
            this.is_filtering = false;
            var tab = '';
            if (this.diarios.length > 0) {
                tab = '#nav-diarios-tab';
            } else if (this.coordenacoes.length > 0) {
                tab = '#nav-coordenacoes-tab';
            } else if (this.praticas.length > 0) {
                tab = '#nav-praticas-tab';
            }
            if (tab != '') {
                setTimeout(() => { jQuery(tab).click() }, 500);
            }
        },
    },
}
