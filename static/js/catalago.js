var carouselWidth = $('.carousel-inner')[0].scrollWidth;
var cardWidth = $('.carousel-item').width();

var scrollPosition = 0;

//Encargado de realizar la animacion de las caratulas
$('.carousel-control-next').on('click', function(){
    
    if (scrollPosition < (carouselWidth - (cardWidth * 4))) {
        console.log('next');
        scrollPosition = scrollPosition + cardWidth;
        $('.carousel-inner').animate({scrollLeft: scrollPosition}, 600);
    }
    
    
   
});