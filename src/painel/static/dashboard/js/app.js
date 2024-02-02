export default {
    compilerOptions: {
        delimiters: ["[[", "]]"],
    },
    data() {
        return {
            destaque: null,
            semestres: [],
            situacoes: [
                { label: "✳️ Diários em andamento", id: "inprogress" },
                { label: "🗓️ Diários a iniciar", id: "future" },
                { label: "📕 Encerrados pelo professor", id: "past" },
                { label: "⭐ Meus diários favoritos", id: "favourites" },
                { label: "♾️ Todos os diários (lento)", id: "allincludinghidden" },
            ],
            ordenacoes: [
                { label: "📗 Ordenado por nome da disciplina", id: "fullname" },
                { label: "🔢 Ordenado por código do diário", id: "shortname" },
                // { "label": "🕓 Ordenado pelo último acessado", "id": "ul.timeaccess desc" },
            ],
            visualizacoes: [
                { label: "Ver como linhas", id: "list" },
                { label: "Ver como cartões", id: "card" },
            ],
            disciplinas: [],
            cursos: [],
            ambientes: [],
            coordenacoes: [],
            praticas: [],
            diarios: [],
            salas: [],
            reutilizaveis: [],
            has_error: false,
            is_filtering: true,
            activeParagraph: null,
            q: localStorage.q || "",
            situacao: localStorage.situacao || "inprogress",
            ordenacao: localStorage.ordenacao || "fullname",
            semestre: localStorage.semestre || "",
            disciplina: localStorage.disciplina || "",
            curso: localStorage.curso || "",
            ambiente: localStorage.ambiente || "",
            contentClosed: localStorage.contentClosed || "true",
            selectedBar: null,
            screenWidth: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
        };
    },

    mounted() {
        if (localStorage.contentClosed == "true") {
            $(".filter-wrapper").addClass("closed");
        }
        $(".view-toggler").change(this.viewToggle);
        $(document).ready(this.customizeAmbiente);
        this.restoreState();
        this.filterCards();
        $("#app").css("display", "block");
        $("#pre-loading").css("display", "none");
        // this.startTour001();
        this.popup();
        window.addEventListener('resize', this.handleResize);
    },
    beforeDestroy() {
         window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        toggleNavBar(e) {
            if (e) {
                e.preventDefault();
            }
            if (localStorage.contentClosed == "true") {
                $(".filter-wrapper").removeClass("closed");
                localStorage.contentClosed = "false";
            } else {
                $(".filter-wrapper").addClass("closed");
                localStorage.contentClosed = "true";
            }
        },

        toggleBar(bar) {
            this.selectedBar = bar;
        },

        // clearFilter() {
        //     $("#q").val('');
        //     $("#situacao").val('');
        //     $("#semestre").val('');
        //     $("#disciplina").val('');
        //     $("#curso").val('');
        //     $("#ambiente").val('');
        // },

        restoreState() {
            let grid_filter = document.getElementById("grid-filter");
            if (grid_filter) {
                grid_filter.classList.remove("hide_this");
                if (!$(".view-toggler").is(":checked")) {
                    const lastView = ["default", "compact"].includes(localStorage.view_toggler)
                        ? localStorage.view_toggler
                        : "default";
                    $("#toggler-" + lastView).prop("checked", true);
                }
            }
        },

        viewToggle() {
            localStorage.view_toggler = $(".view-toggler:checked").val();
            $(".courses").removeClass("default compact").addClass(localStorage.view_toggler);
        },

        customizeAmbiente() {
            // $("#ambiente, #curso, #disciplina, #semestre").select2({
            //     templateSelection: function (data) {
            //         const style = 'style="padding: 0 5px 0 30px; color: #1D2125; "';
            //         return $("<span " + style + ">" + data.text + "</span> ");
            //     },
            // });
            $("#semestre").select2({
                placeholder: "<i class='icon icon-calendario-semestre'></i> Semestres...",
                templateSelection: function (data) {
                    const style = 'style="color: #1D2125; "';
                    
                    return $("<span " + style + ">" + data.text + "</span> ");
                },
            });
             $("#disciplina").select2({
                placeholder: "<i class='icon icon-disciplina'></i> Disciplinas...",
                templateSelection: function (data) {
                    const style = 'style="color: #1D2125; "';
                    
                    return $("<span " + style + ">" + data.text + "</span> ");
                },
            });
             $("#curso").select2({
                placeholder: "<i class='icon icon-icone-ava'></i> Cursos...",
                templateSelection: function (data) {
                    const style = 'style="color: #1D2125; "';
                    
                    return $("<span " + style + ">" + data.text + "</span> ");
                },
            });
            $("#ambiente").select2({
                placeholder: "<i class='icon icon-moodle'></i> Ambientes...",
                templateSelection: function (data) {
                    const style = 'style="color: #1D2125; "';
                    
                    return $("<span " + style + ">" + data.text + "</span> ");
                },
            });
            $("#situacao").select2({
                templateSelection: function (data) {
                    const style = 'style="padding: 0 5px 0 0px; color: #1D2125; "';
                    return $("<span " + style + ">" + data.text + "</span> ");
                },
            });
            
            setTimeout(function () {
                $("#ambiente").val($("#ambiente option:eq(0)").val()).trigger("change");
                $("#curso").val($("#curso option:eq(0)").val()).trigger("change");
                // $('#situacao').val($('#situacao option:eq(0)').val()).trigger('change');
                $("#disciplina").val($("#disciplina option:eq(0)").val()).trigger("change");
                $("#semestre").val($("#semestre option:eq(0)").val()).trigger("change");

                // Código usado para adicionar o filtro verde no select2.

                $("#semestre").on("change", function () {
                    // Se o texto selecionado for diferente de 'Semestres...'
                    if ($("#semestre :selected").text() !== "Semestres...") {
                        // Adicione a classe ao elemento desejado
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-semestre-container"]'
                        ).addClass("filter-active");
                    } else {
                        // Caso contrário, remova a classe
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-semestre-container"]'
                        ).removeClass("filter-active");
                    }
                });
                $("#disciplina").on("change", function () {
                    // Se o texto selecionado for diferente de 'Semestres...'
                    if ($("#disciplina :selected").text() !== "Disciplinas...") {
                        // Adicione a classe ao elemento desejado
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-disciplina-container"]'
                        ).addClass("filter-active");
                    } else {
                        // Caso contrário, remova a classe
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-disciplina-container"]'
                        ).removeClass("filter-active");
                    }
                });
                $("#curso").on("change", function () {
                    // Se o texto selecionado for diferente de 'Semestres...'
                    if ($("#curso :selected").text() !== "Cursos...") {
                        // Adicione a classe ao elemento desejado
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-curso-container"]'
                        ).addClass("filter-active");
                    } else {
                        // Caso contrário, remova a classe
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-curso-container"]'
                        ).removeClass("filter-active");
                    }
                });
                $("#ambiente").on("change", function () {
                    // Se o texto selecionado for diferente de 'Semestres...'
                    if ($("#ambiente :selected").text() !== "Ambientes...") {
                        // Adicione a classe ao elemento desejado
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-ambiente-container"]'
                        ).addClass("filter-active");
                    } else {
                        // Caso contrário, remova a classe
                        $(
                            'span.select2-selection.select2-selection--single[aria-labelledby="select2-ambiente-container"]'
                        ).removeClass("filter-active");
                    }
                });
            }, 100);

            function adicionarClasseAoSpan(select2Id, classe) {
                $(select2Id).on("select2:select", function () {
                    var spanElement = $(this).next(".select2-container").find(".select2-selection");
                    spanElement.addClass(classe);
                });
            }
            adicionarClasseAoSpan("#ambiente", "bgcolor-select2");
            adicionarClasseAoSpan("#curso", "bgcolor-select2");
        },

        startTour001() {
            const geral = this;
            if (localStorage.getItem("completouTour001") != "true") {
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
                        element: "#dropdownMenuSuporte",
                        title: "Precisa de ajuda?",
                        content: "Aqui você tem um lista de canais para lhe ajudarmos.",
                        placement: "bottom-end",
                    },
                    {
                        element: "#all-notifications",
                        title: "Avisos",
                        content:
                            "Aqui você verá quantas <strong>notificações</strong> e <strong>mensagens</strong> existem em cada AVA.",
                        placement: "bottom-end",
                    },
                    {
                        element: ".header-user",
                        title: "Menu usuário",
                        content: "Acesse seu perfil no SUAP ou saia do Painel AVA de forma segura.",
                        placement: "left",
                    },
                    {
                        element: "#sidebar",
                        title: "Filtros",
                        content:
                            "<p>Aqui você pode filtrar diários por semestre, curso, turma, disciplina, código/id do diário, curso, ambiente (AVA) ou situação, além de poder ordenar como será visto.</p><p>Você pode começar digitando o nome da disciplina e pressionando [ENTER] como uma primeira procura.</p>",
                        placement: "right",
                        onNext: function () {
                            $("#toggler-default").prop("checked", true);
                            geral.viewToggle();
                        },
                    },
                ]);
                wt.start();
                localStorage.setItem("completouTour001", true);
            }
        },

        popup() {
            $(function () {
                if (!window.popupModalName) {
                    return;
                }
                const lastOccurrence = new Date(localStorage.getItem(window.popupModalName));

                // Já respondeu
                if (isNaN(lastOccurrence)) {
                    return;
                }

                // O oopup nunca foi visto ou se passaram 12h desde a última visualização sem responder
                if ((new Date() - lastOccurrence) / (1000 * 3600 * 12) > 1) {
                    new bootstrap.Modal(document.getElementById(popupModalName)).toggle();
                }

                // Se fechar sem clicar no link pede para repetir em 12h
                $("#" + popupModalName).on("hidden.bs.modal", function () {
                    localStorage.setItem(popupModalName, new Date().toISOString());
                    console.log("closeModalUntilTomorrow");
                });

                $("#model-url").on("click", function closeModalForever(e) {
                    $("#modal1").click();
                    localStorage.setItem(popupModalName, "true");
                    window.open(popupModalUrl);
                });
            });
        },

        favourite(card) {
            const new_status = card.isfavourite ? 0 : 1;
            axios
                .get("/painel/api/v1/set_favourite/", {
                    params: {
                        ava: card.ambiente.titulo,
                        courseid: card.id,
                        favourite: new_status,
                    },
                })
                .then((response) => {
                    card.isfavourite = new_status == 1;
                })
                .catch((error) => {
                    console.debug(error);
                });
        },

        visible(card) {
            if (confirm("Confirma a operação?")) {
                const new_status = parseInt(card.visible) ? 0 : 1;
                axios
                    .get("/painel/api/v1/set_visible/", {
                        params: {
                            ava: card.ambiente.titulo,
                            courseid: card.id,
                            visible: new_status,
                        },
                    })
                    .then((response) => {
                        card.visible = new_status == 1;
                    })
                    .catch((error) => {
                        console.debug(error);
                    });
            }
        },

        cardActionsToggler(event) {
            let item = $(event.srcElement).parent().parent().parent().parent();
            console.log(item)
            if ($(item).hasClass("showActions")) {
                
                $(item).removeClass("showActions");
                $(event.srcElement).removeClass("favorited");
            } else {
                
                $(item).addClass("showActions ");
                $(event.srcElement).addClass(" favorited");
                
            }
        },

        clearFilter() {
            this["q"] = "";
            $("#situacao").val("inprogress").trigger("change");
            $("#ordenacao").val("fullname").trigger("change");
            $("#semestre").val("").trigger("change");
            $("#disciplina").val("").trigger("change");
            $("#curso").val("").trigger("change");
            $("#ambiente").val("").trigger("change");
            // setTimeout(this.filterCards, 500);
            $(".select2-selection").removeClass("bgcolor-select2");
        },

        clearFilterSeeAll() {
            console.log(this.$watch);
            this["q"] = "";
            this["situacao"] = "allincludinghidden";
            this["ordenacao"] = "fullname";
            this["semestre"] = "";
            this["disciplina"] = "";
            this["curso"] = "";
            this["ambiente"] = "";
            // setTimeout(this.filterCards, 500);
            $(".select2-selection").removeClass("bgcolor-select2");
        },

        filterCards() {
            this.filtering();
            try {
                axios
                    .get("/painel/api/v1/diarios/", {
                        params: {
                            q: $(self.q).val() || localStorage.q || "",
                            situacao: $("#situacao").val() || localStorage.situacao || "inprogress",
                            ordenacao: $(self.ordenacao).val() || localStorage.ordenacao || "fullname",
                            semestre: $(self.semestre).val() || localStorage.semestre || "",
                            disciplina: $(self.disciplina).val() || localStorage.disciplina || "",
                            curso: $(self.curso).val() || localStorage.curso || "",
                            ambiente: $(self.ambiente).val() || localStorage.ambiente || "",
                        },
                    })
                    .then((response) => {
                        Object.assign(this, response.data);
                        this.filtered();
                    })
                    .catch((error) => {
                        this.has_error = true;
                        this.filtered();
                        return Promise.reject(error);
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
            this.reutilizaveis = [];
            this.has_error = false;
            this.is_filtering = true;
        },

        filtered() {
            this.viewToggle();
            this.restoreState();
            this.is_filtering = false;
            var tab = "";
            if (this.diarios.length > 0) {
                tab = "#nav-diarios-tab";
            } else if (this.coordenacoes.length > 0) {
                tab = "#nav-coordenacoes-tab";
            } else if (this.praticas.length > 0) {
                tab = "#nav-praticas-tab";
            } else if (this.reutilizaveis.length > 0) {
                tab = "#nav-reutilizaveis-tab";
            }
            if (tab != "") {
                setTimeout(() => {
                    jQuery(tab).click();
                }, 500);
            }
        },

        get_situacao_desc() {
            return $("#situacao option:selected").text();
        },

        get_ordenacao_desc() {
            return $("#ordenacao option:selected").text();
        },

        go_to_suap() {
            $("#syncs").modal("show");
        },

        go_to_coordanation() {
            $("#syncs").modal("show");
        },

        go_to_grades() {
            $("#syncs").modal("show");
        },

        go_to_grades_preview() {
            $("#syncs").modal("show");
        },

        go_to_sync_logs() {
            $("#syncs").modal("show");
        },

        isFromSUAP(diario) {
            return diario != null && Object.hasOwn(diario, "id_diario_clean");
        },
        handleResize() {
            this.screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        },
        handleSelectChange(event) {
            console.log('teste');
            var selectedValue = event.target.value;
            // Adicione a lógica necessária com base na opção selecionada
            this.toggleBar(selectedValue);
            },
            // Se necessário, adicione a lógica do método toggleBar
            toggleBar(selectedValue) {
            // Lógica para manipular o estado com base na opção selecionada
            //console.log('Toggle bar:', selectedValue);
        }
    },

    watch: 
    {
        q(newValue) {
            localStorage.q = newValue || "";
        },
        situacao(newValue) {
            localStorage.situacao = newValue || "inprogress";
        },
        ordenacao(newValue) {
            localStorage.ordenacao = newValue || "fullname";
        },
        semestre(newValue) {
            localStorage.semestre = newValue || "";
        },
        disciplina(newValue) {
            localStorage.disciplina = newValue || "";
        },
        curso(newValue) {
            localStorage.curso = newValue || "";
        },
        ambiente(newValue) {
            localStorage.ambiente = newValue || "";
        },
    },





};


