document.addEventListener('DOMContentLoaded', () => {
  new Swiper('.card__carousel', {
    direction: 'horizontal',
    loop: true,
    pagination: {
      el: '.swiper-pagination',
    },
  });
})