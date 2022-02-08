    // Primeiro Carousel
    $('.loop--nav').find('.next').click(() => {
        var item = $('.owl-carousel .owl-stage-outer .owl-stage .owl-item.active');
        console.log("Item: "+item);
        var index = item.index() -4;
        console.log("Index: "+index);
        
        if(index == 6){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(2)').addClass('active');
        }else if(index == 11){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(3)').addClass('active');
        }else if(index == 16){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(4)').addClass('active');
        }else if(index == 21){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(5)').addClass('active');
        }else if(index == 1){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(1)').addClass('active');
        }
    
      });
    
      $('.loop--nav').find('.prev').click(() => {
        var item = $(' .owl-carousel .owl-stage-outer .owl-stage .owl-item.active');
        console.log("Item: "+item);
        var index = item.index() -4;
        console.log("Index: "+index);
        
        if(index == 1 || index == 5){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(1)').addClass('active');
        }else if(index == 6 || index == 10){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(2)').addClass('active');
        }else if(index == 11 || index == 15){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(3)').addClass('active');
        }else if(index == 16 || index == 20){
          $('.indicator').removeClass('active');
          $('.indicator:nth-child(4)').addClass('active');
        }
    
      });
    
    
      // Segundo carousel
    
      $('.loop--nav2').find('.next2').click(() => {
        var item = $('.teste4 .owl-carousel .owl-stage-outer .owl-stage .owl-item.active');
        console.log("Item: "+item);
        var index = item.index() -4;
        console.log("Index: "+index);
        
        if(index == 6){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(2)').addClass('active');
        }else if(index == 11){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(3)').addClass('active');
        }else if(index == 16){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(4)').addClass('active');
        }else if(index == 21){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(5)').addClass('active');
        }else if(index == 1){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(1)').addClass('active');
        }
    
      });
    
      $('.loop--nav2').find('.prev2').click(() => {
        var item = $('.owl-carousel .owl-stage-outer .owl-stage .owl-item.active');
        console.log("Item: "+item);
        var index = item.index() -4;
        console.log("Index: "+index);
        
        if(index == 1 || index == 5){
          $('.indicator2').removeClass('active');
          $('.indicator:nth-child(1)').addClass('active');
        }else if(index == 6 || index == 10){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(2)').addClass('active');
        }else if(index == 11 || index == 15){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(3)').addClass('active');
        }else if(index == 16 || index == 20){
          $('.indicator2').removeClass('active');
          $('.indicator2:nth-child(4)').addClass('active');
        }
    
      });    