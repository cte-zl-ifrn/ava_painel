

 

$(document).ready(function() {

    // setTimeout( function(){
    
   
    //     $('#disciplina_id').select2({
    //         width: '100%',
    //         height: '100%',
    //     });
   
   
   
    // },10000);
    $('#disciplina_id').select2({
        width: '100%',
        height: '100%',
    });


    // $('#status_id').select2({
    //     width: '100%',
    //     height: '100%'
    // });

    // $('#competencia_id').select2({
    //     width: '100%',
    //     height: '100%'
    // });
    
    $('.select2-selection').css('border-radius','0px')
    $('.select2-container').children().css('border-radius','0px')
});