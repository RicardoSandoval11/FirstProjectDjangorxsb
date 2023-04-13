$(document).ready(function(){

  //Menu effect

  $(".nav-item").each(function(index, element){
    $(this).css({
          marginTop:"-200px"
      });

      $(this).animate({
        //top: "0"
        marginTop: '10px'
    }, 500 + (index*500));
  });

  //Main categories effect

    $(".woman").css({
      display:"none"
    });

    $(".man").css({
      display:"none"
    });

    $('.woman').fadeIn(1000);
    $('.man').fadeIn(1000);

    $("#categories-woman").hide();
    $(".categories-man").hide();

    // Categories option effect
    $('.woman').click(function () {
      $("#categories-woman").slideToggle();
    });

    // Categories option effect
    $('.man').click(function () {
      $(".categories-man").slideToggle();
    });
    

});
