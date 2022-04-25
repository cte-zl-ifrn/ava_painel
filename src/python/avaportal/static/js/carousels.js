const carouselDeCima = $('.loop');
carouselDeCima.owlCarousel({
    center: false,
    items: 1,
    loop: true,
    margin: 20,
    autoplay: false,
    autoplayTimeout: 50000,
    autoplaySpeed: 1000,
    autoplayHoverPause: true,
    responsive: {
        360: {
            items: 1,
            margin: -55
        },
        720: {
            items: 2,
        },
        860: {
            items: 3
        },
        996: {
            items: 4
        },
        1280: {
            items: 5
        },
        1660: {
            items: 6
        }
    }
});

const carouselDeCimaNav = $('.loop--nav');

carouselDeCimaNav.find('.prev').click(() => {
    carouselDeCima.trigger('prev.owl.carousel');
});
carouselDeCimaNav.find('.next').click(() => {
    carouselDeCima.trigger('next.owl.carousel');
});


const carouselDeBaixo = $('.loop2');
carouselDeBaixo.owlCarousel({
    center: false,
    items: 1,
    loop: true,
    margin: 20,
    autoplay: false,
    autoplayTimeout: 50000,
    autoplaySpeed: 1000,
    autoplayHoverPause: true,
    responsive: {
        360: {
            items: 1,
            margin: -55
        },
        720: {
            items: 2,
        },
        860: {
            items: 3
        },
        996: {
            items: 4
        },
        1280: {
            items: 5
        },
        1660: {
            items: 6
        }
    }
});

const carouselDeBaixoNav = $('.loop--nav2');

carouselDeBaixoNav.find('.prev2').click(() => {
    carouselDeBaixo.trigger('prev.owl.carousel');
});
carouselDeBaixoNav.find('.next2').click(() => {
    carouselDeBaixo.trigger('next.owl.carousel');
});
