// надо считать, получить доступ къ кнопке
const topBtn = document.querySelector(".go-top");


// прокрут окна
window.addEventListener("scroll", trackScroll);
// реакция на нажатие
window.addEventListener("click", goTop);

function trackScroll() {
    // должна появляться, когда прокручено больше одного экрана
    // смотрим положение от верха окна прокрута
    const scrolled = window.pageYOffset;
    console.log(scrolled);
    // высота окна браузера
    const winHi = document.documentElement.clientHeight;
    // коли прокрутили более одного экрана
    if (scrolled > winHi) {
        // должна показаться кнопка
//        topBtn.classList.add("go-top--show");
        topBtn.style.display = "block";
    } else {
        // или исчезает
//        topBtn.classList.remove("go-top--show");
        topBtn.style.display = "none";
    }
}

function goTop() {
    // пока не вернулись до начала страницы
    if (window.pageYOffset > 0) {
        // прокрут к верху
        window.scrollBy(0, -288); // аргументы скорости по X / Y
        setTimout(goTop, 0);    // скорость кручения в милисекундах
    }
}