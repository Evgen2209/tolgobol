var swiper = new Swiper( '.feedback-slide', {
    //стрелки
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },
    //навигация
    //буллеты, текущее положение, прогрессбар
    pagination: {
        el: '.swiper-pagination',
        // буллеты
        clickable: true,
        // динамические буллеты
        dynamicBullets: true,
    },
    slidesPerView: 1,
} ); 