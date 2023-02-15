export default {
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data() {
        return {
            "atualizacoes": [],
            "unread_notification_total": 0,
            "unread_conversations_total": 0
        }
    },
    mounted() {
        this.showAtualizacoes();
    },
    methods: {
        showAtualizacoes: function() {
            axios.get(
                '/portal/api/v1/atualizacoes_counts/', {params: {}}
            ).then(response => {
                Object.assign(this, response.data);
            });
        },
    },
}

$(document).ready(function(){                          
    $('#notifications-drawer').click(function(e){  
        $("#box2").hide();
        if ($('#box:visible').length) {
            $("#box").hide();
        } else {
            $("#box").show();
        }
    });       
});

$(document).ready(function(){                          
    $('#messagen-drawer').click(function(e){  
        $("#box").hide();
        if ($('#box2:visible').length) {
            $("#box2").hide();
        } else {
            $("#box2").show();
        }
    });       
});