String.prototype.toDOM=function(){
    var d=document
       ,i
       ,a=d.createElement("div")
       ,b=d.createDocumentFragment();
    a.innerHTML=this;
    while(i=a.firstChild)b.appendChild(i);
    return b;
  };
function getAllUrlParams(url) {
// извлекаем строку из URL или объекта window
var queryString = url ? url.split('?')[1] : window.location.search.slice(1);
// объект для хранения параметров
var obj = {};
// если есть строка запроса
if (queryString) {
    // данные после знака # будут опущены
    queryString = queryString.split('#')[0];

    // разделяем параметры
    var arr = queryString.split('&');

    for (var i=0; i<arr.length; i++) {
    // разделяем параметр на ключ => значение
    var a = arr[i].split('=');
    // обработка данных вида: list[]=thing1&list[]=thing2
    var paramNum = undefined;
    var paramName = a[0].replace(/\[\d*\]/, function(v) {
        paramNum = v.slice(1,-1);
        return '';
    });
    // передача значения параметра ('true' если значение не задано)
    var paramValue = typeof(a[1])==='undefined' ? true : a[1];
    // преобразование регистра
    paramName = paramName.toLowerCase();
    paramValue = paramValue.toLowerCase();   
    // если ключ параметра уже задан
    if (obj[paramName]) {
        // преобразуем текущее значение в массив
        if (typeof obj[paramName] === 'string') {
        obj[paramName] = [obj[paramName]];
        }
        // если не задан индекс...
        if (typeof paramNum === 'undefined') {
        // помещаем значение в конец массива
        obj[paramName].push(paramValue);
        }
        // если индекс задан...
        else {
        // размещаем элемент по заданному индексу
        obj[paramName][paramNum] = paramValue;
        }
    }
    // если параметр не задан, делаем это вручную
    else {
        obj[paramName] = paramValue;
    }
    }
}
return obj;
}  

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function register_init() {
    var target = document.getElementById("register");
    if( !target )
        return
    target.onclick =
        function(e){
            approval = document.getElementById("approval")
            if( !approval.checked )
            {
                approval.parentNode.classList.add( 'red_border' )
                return
            }
            email = document.getElementById("email").value
            auth_data = {
                "adres": document.getElementById("adres").getAttribute('name'),
                "first_name": document.getElementById("first_name").value,
                "last_name": document.getElementById("last_name").value,
                "patronymic": document.getElementById("patronymic").value,
                "male": document.getElementById("male").getAttribute('name'),
                "username": document.getElementById("username").value,
                "password1": document.getElementById("password1").value,
                "password2": document.getElementById("password2").value,
                "birthday": document.getElementById("birthday").value,
                "telephon": document.getElementById("telephon").value,
                "approval": approval.checked,
            }
            if( email )
            {
                auth_data.email = email
                console.log(email, 'emailss')
            }
            url_param = getAllUrlParams()
            console.log(url_param, 'url_param')
            if( url_param.invite )
            {
                auth_data.invite = url_param.invite
            }
            $.ajax({
                url: '/auth/authservice/',
                method: 'post',
                dataType: 'html',
                data: auth_data,
                headers: {
                    "X-Requested-MethodName": "AuthService.Register"
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function(data){
                    var json_data = JSON.parse(data);
                    if( 'errors' in json_data ) 
                    {
                        for( nam in json_data['errors'] )
                        {
                            error = document.getElementsByClassName('error_text')
                            var i;
                            for (i = 0; i < error.length; i++)
                            {
                                error[i].remove()
                            }
                            var new_el = document.createElement("p");
                            new_el.innerHTML = json_data['errors'][nam];
                            new_el.className = 'error_text';
                            var el = document.getElementById(nam);
                            el.parentNode.insertBefore(new_el, el.nextSibling);
                        }
                    }
                    else
                    {
                        var el = document.getElementById('register_form');
                        var panel =  el.parentNode;
                        panel.innerHTML = '';

                        var new_el_dev = document.createElement("dev");
                        new_el_dev.className = 'success_text';

                        var new_el_p = document.createElement("p");
                        new_el_p.innerHTML = 'Регистрация прошла успешно.';
                        new_el_p.className = 'success_text';

                        new_el_dev.appendChild( new_el_p );
                        panel.appendChild(new_el_dev);
                    }
        
                },
                error: function(er) {
                    console.log(er);
                }
            });        
        }
}

function savege_auth()
{
    btn = document.getElementById('save_btn_auth')
    if( !btn )
        return
    btn.onclick = function()
    {
        first_name = document.getElementById('first_name')
        last_name = document.getElementById('last_name')
        patronymic = document.getElementById('patronymic')
        birthday = document.getElementById('birthday')
        email = document.getElementById('email')
        telephon = document.getElementById('telephon')
      $.ajax({
        url: '/auth/authservice/',
        method: 'post',
        dataType: 'json',
        data: {
            "first_name": first_name.value,
            "last_name": last_name.value,
            "patronymic": patronymic.value,
            "birthday": birthday.value,
            "email": email.value,
            "telephon": telephon.value,
        },
        headers: {
            "X-Requested-MethodName": "AuthService.ChangeUserData"
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(data){
            if( data.errors ) 
            {
                console.log(data.errors);
                for( nam in data.errors )
                {
                    error = document.getElementsByClassName('error_text')
                    var i;
                    for ( i = 0; i < error.length; i++ )
                    {
                        error[i].remove()
                    }
                    var new_el = document.createElement("p");
                    new_el.innerHTML = data.errors[nam];
                    new_el.className = 'error_text';
                    var el = document.getElementById(nam);
                    el.value = ''
                    el.parentNode.insertBefore(new_el, el.nextSibling);
                }
            }
            else
            {
                for( i in data )
                {
                    el = document.getElementById(i)
                    el.value = data[i]
                }
                btn_save = document.getElementById('change_btn_auth')
                btn_save.classList.toggle('show')
                btn.classList.toggle('show')
            }
        },
        error: function(er) {
            console.log( "Запрос: /auth/authservice/" );
            console.log(er);
        }
    });      
    }
}

function change_auth(){
    btn = document.getElementById('change_btn_auth')
    if( !btn )
        return
    btn.onclick = function()
    {
        first_name = document.getElementById('first_name')
        last_name = document.getElementById('last_name')
        patronymic = document.getElementById('patronymic')
        birthday = document.getElementById('birthday')
        email = document.getElementById('email')
        telephon = document.getElementById('telephon')
        first_name.disabled = false
        last_name.disabled = false
        patronymic.disabled = false
        birthday.disabled = false
        email.disabled = false
        telephon.disabled = false
        btn_save = document.getElementById('save_btn_auth')
        btn_save.classList.toggle('show')
        btn.classList.toggle('show')
    }
}

function feedback_adres(){
    btn = document.getElementById('feedback_adres')
    btn.onclick = function()
    {
        var overlay = document.createElement("dev");
        overlay.className = 'fixed-overlay';
        overlay.classList.add('fixed-overlay__modal');
        overlay.id = "overlay-modal";

    
        var modal = document.createElement("dev");
        modal.className = 'modal';

        var modal_container = document.createElement("dev");
        modal_container.className = 'modal_container';
      
      
        var close_el = document.createElement("img");
        close_el.src = "/static/images/close.png";
        close_el.setAttribute( 'href', "/static/images/close.png" )
        close_el.className = "modal__cross";
        close_el.onclick = function() {
          modal.remove();
          overlay.remove();
          document.body.classList.toggle('_lock')
        }
      
        var p = document.createElement("p");
        p.className = "modal__title";
        p.innerText = 'Укажите пожалуйста название улици, номер дома и квартиру если есть';
      
        adres = document.createElement('input')
        adres.classList.add('input')
        adres.setAttribute('placeholder', 'Адрес')
        name_fio = document.createElement('input')
        name_fio.classList.add('input')
        name_fio.setAttribute('placeholder', 'Как к вам обращаться')
        contact = document.createElement('input')
        contact.classList.add('input')
        contact.setAttribute('placeholder', 'Как с вами связаться')
        comment = document.createElement('textarea')
        comment.classList.add('textarea')
        comment.classList.add('input')
        comment.setAttribute('placeholder', 'Комментарий')

        btn = document.createElement('button')
        btn.classList.add('button')
        btn.innerText = "Отправить"
        
        modal_container.appendChild( close_el );
        modal_container.appendChild( p );
        modal_container.appendChild( adres );
        modal_container.appendChild( name_fio );
        modal_container.appendChild( contact );
        modal_container.appendChild( comment );
        modal_container.appendChild( btn );
        modal.appendChild( modal_container );
        overlay.appendChild( modal );
        document.body.classList.toggle('_lock')
        document.body.appendChild( overlay );
        btn.onclick = function()
        {
            $.ajax({
                url: '/mainservise/',
                method: 'post',
                dataType: 'json',
                data: {
                    adres: adres.value,
                    name: name_fio.value,
                    contact: contact.value,
                    comment: comment.value
                },
                headers: {
                    "X-Requested-MethodName": "MainService.FeedbackAdres"
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function(data){
                    if( data.errors ) 
                    {
                    }
                    else
                    {
                        modal.remove();
                        overlay.remove();
                        document.body.classList.toggle('_lock')
              
                    }
        
                },
                error: function(er) {
                    console.log(er);
                }
            });   
        }
    }
}

function init() {
    register_init();
    savege_auth();
    change_auth();
    feedback_adres();
    el = document.querySelector(".feedback_adres")
    if( el )
    {
        el.insertAdjacentElement( 'beforeBegin', create_adres_component() )
    }
}
init();