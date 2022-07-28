/* Когда пользователь нажимает на кнопку, переключаться раскрывает содержимое */
function drop_list(sorce) {
    var is_class = sorce.nextElementSibling.classList.contains('show');
    var dropdowns = document.getElementsByClassName("drop-list-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        openDropdown.classList.remove('show');
        openDropdown.previousElementSibling.classList.remove('_open');

    }
    if ( !is_class )
    {
        sorce.nextElementSibling.classList.toggle("show");
        sorce.classList.toggle("_open");
    }
}
  
  // Закрыть раскрывающийся список, если пользователь щелкнет за его пределами.
window.onclick = function(event) {
    if (!event.target.matches('.drop-list-btn')) {
        var dropdowns = document.getElementsByClassName("drop-list-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
            openDropdown.previousElementSibling.classList.remove('_open');
            openDropdown.parentElement
        }
        }
    }
}
function checkout_list(source) {
    source.parentElement.previousElementSibling.innerHTML  = source.text;
}