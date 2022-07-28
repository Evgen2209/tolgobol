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

function get_adre() {
    strit_id = document.getElementById("strit_id").name;
    houss = document.getElementById("hous_id").getAttribute('name');
    gous_el = document.getElementById("kv_id").getAttribute('name');
    qweri = 'strit_id='+strit_id + '&hous=' + houss;
    if( gous_el )
    {
        qweri = qweri + '&kv=' + gous_el
    }
    $.ajax( {
        // запрос на список квартир
        url: '/auth/authservice/?' + qweri,
        method: 'get',
        dataType: 'json',
        data: $(this).serialize(),
        headers: {
            "X-Requested-MethodName": "AuthService.GetAdres"
        },
        success: function(data) 
        {
            if( data.error ) {
                console.log( data.error );
                return;
            }
            adres = data.adres
            if( adres.length == 1 )
            {
                el_adres = document.getElementById("adres");
                el_adres.setAttribute( 'name', adres[0].id )
            }
        },
        error: function(er)
        {
            console.log(er);
        }
    } )
}

function checkout_kv(source){
    source.parentElement.previousElementSibling.setAttribute('name',  source.text)
    source.parentElement.previousElementSibling.innerHTML  = source.text;
    get_adre();
}

function checkout_hous(source) {
    source.parentElement.previousElementSibling.setAttribute('name',  source.text) 
    source.parentElement.previousElementSibling.innerHTML  = source.text;
    el_kv_id = document.getElementById("kv_id")
    el_kv_id.removeAttribute('name');
    el_kv_id.innerHTML = 'Кв'
    el_kv_id.nextElementSibling.innerHTML = ''
    $.ajax( {
        // запрос на список квартир
        url: '/auth/authservice/?strit_id='+source.id + '&hous=' + source.text,
        method: 'get',
        dataType: 'json',
        data: $(this).serialize(),
        headers: {
            "X-Requested-MethodName": "AuthService.GetAdres"
        },
        success: function(data) 
        {
            list = document.getElementById("drop_list_content_kv");
            list.innerHTML = '';
            if( data.error ) {
                console.log( data.error );
                return;
            }
            adres = data.adres
            if( adres.length == 0 )
            {
                var el = document.createElement('a')
                el.innerHTML = 'нет'
                list.appendChild( el );
                get_adre();
            }
            for ( var key in adres ) {
                //redakt
                var el = '<a id="' + adres[key].id + '" onclick="checkout_kv(this)">'+adres[key].kv+'</a>';
                list.appendChild( el.toDOM() );
            }
            //get_adre(source.text);
        },
        error: function(er)
        {
            console.log(er);
        }
    } )
    
}

function checkout_strit(source) {
    source.parentElement.previousElementSibling.name = source.id;
    source.parentElement.previousElementSibling.innerHTML  = source.text;

    String.prototype.toDOM=function(){
        var d=document
           ,i
           ,a=d.createElement("div")
           ,b=d.createDocumentFragment();
        a.innerHTML=this;
        while(i=a.firstChild)b.appendChild(i);
        return b;
      };
    $.ajax({
		url: '/auth/authservice/?strit_id='+source.id,
		method: 'get',
		dataType: 'json',
		data: $(this).serialize(),
        headers: {
            "X-Requested-MethodName": "AuthService.GetAdres"
        },
		success: function(data){
            strit_id = document.getElementById("strit_id");
            strit_id.setAttribute('name', source.id) 
            list = document.getElementById("drop_list_content_house");
            list.innerHTML = '';
            if( data.error ) {
                console.log( data.error );
                return;
            }
            adres = data.adres
            for ( var key in adres ) {
                var el = '<a id="' + adres[key].id + '" onclick="checkout_hous(this)">'+adres[key].hous+'</a>';
                list.appendChild( el.toDOM() );
            }
		},
        error: function(er) {
            console.log(er);
        }
    });
}

// document.getElementsByClassName('birthday')[0].onkeyup = function(e) {
// if (e.target.value.length == 2 || e.target.value.length == 5) {
//     e.target.value += '.';
// }
// };

list = document.getElementsByClassName('gender_input')
for( i in list )
{
    list[i].onclick = function() {
        value = this.getAttribute('value')
        this.parentElement.setAttribute('name', value)
    }
}