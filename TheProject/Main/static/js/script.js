$(document).ready(function(){
    $(".fancybox").fancybox({
          openEffect: "none",
          closeEffect: "none"
      });
      
      $(".zoom").hover(function(){
          
          $(this).addClass('transition');
      }, function(){
          
          $(this).removeClass('transition');
      });
  });

$(document).ready(function() {
// Listen for the show.bs.collapse event on .navbar-collapse
$('.navbar-collapse').on('show.bs.collapse', function() {
    // When the dropdown menu is shown, remove the rounded corners from .navbar
    $('.navbar').css({
    'border-bottom-left-radius': '0',
    'border-bottom-right-radius': '0'
    });
});

// Listen for the hide.bs.collapse event on .navbar-collapse
$('.navbar-collapse').on('hide.bs.collapse', function() {
    // When the dropdown menu is hidden, restore the rounded corners to .navbar
    setTimeout(function() {
        $('.navbar').css({
          'border-bottom-left-radius': '15px',
          'border-bottom-right-radius': '15px'
        });
      }, 250);
});
});