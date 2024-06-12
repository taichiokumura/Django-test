let currentSlide = 0;

function moveSlide(step) {
    const slides = document.querySelector('.slides');
    const totalSlides = document.querySelectorAll('.slide').length;

    currentSlide = (currentSlide + step + totalSlides) % totalSlides;
    const offset = -currentSlide * 100;

    slides.style.transform = `translateX(${offset}%)`;
}

//スライドにクリックイベントを追加して遷移する
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.slide img').forEach((image, index) => {
        image.addEventListener('click', () => {
            let location = '';
            if (index == 0) {
                location = 'upstream';
            } else if (index == 1) {
                location = 'midstream';
            } else if (index == 2) {
                location = 'downstream';
            }
            window.location.href = `/map/${location}/`;
        });
    });
});