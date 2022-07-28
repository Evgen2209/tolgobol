
function get_csrftoken(name) 
{
    name = 'csrftoken';
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

function send_ajax( url, data, method_name, func_success )
{
    $.ajax( {
        url: url,
        method: 'post',
        dataType: 'json',
        data: data,
        headers: {
            "X-Requested-MethodName": method_name
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", get_csrftoken());
        },
        success: func_success,
        error: function(er)
        {
            console.log( er );
        }
    } )

}

function create_modal(element)
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

  modal_container.appendChild( close_el );
  // добавление переданного элимента
  modal_container.appendChild( element );
  modal.appendChild( modal_container );
  overlay.appendChild( modal );
  document.body.classList.toggle('_lock')
  document.body.appendChild( overlay );
}

function get_months()
{
    data = [
        {name:'Январь', id: 1},
        {name:'Февраль', id: 2},
        {name:'март', id: 3},
        {name:'Апрель', id: 4},
        {name:'Май', id: 5},
        {name:'Июнь', id: 6},
        {name:'Июль', id: 7},
        {name:'Август', id: 8},
        {name:'Сентябрь', id: 9},
        {name:'Октябрь', id: 10},
        {name:'Ноябрь', id: 11},
        {name:'Декабрь', id: 12},
    ]
    month_el = document.createElement( 'div' )
    month_el.classList.add('drop-list');
    month_el.classList.add('months');

    btn_month_el = document.createElement( 'div' )
    btn_month_el.classList.add('drop-list-btn');
    btn_month_el.classList.add('months');
    btn_month_el.innerText = "месяц"

    content_month_el = document.createElement( 'div' )
    content_month_el.classList.add('drop-list-content');
    content_month_el.classList.add('months');
    

    btn_month_el.onclick = function()
    {
        if( this.classList.contains( '_open' ) && this.nextSibling.classList.contains( 'show' ) )
        {
            set_dtn = document.getElementsByClassName( 'drop-list-content' )
            for( let i of set_dtn )
            {
                i.classList.remove( 'show' )
                i.previousSibling.classList.remove( '_open' )
            }
            this.classList.remove( '_open' )
            this.nextSibling.classList.remove( 'show' )    
            console.log('ЕСТЬ')
        }
        else
        {
            set_dtn = document.getElementsByClassName( 'drop-list-content' )
            for( let i of set_dtn )
            {
                i.classList.remove( 'show' )
                i.previousSibling.classList.remove( '_open' )
            }
            this.classList.add( '_open' )
            this.nextSibling.classList.add( 'show' )
            console.log('НЕТ')
        }
    }
    for( let i of data )
    {
        a = document.createElement( 'a' )
        a.setAttribute( 'id', i.id );
        a.innerText = i.name
        a.onclick = function()
        {
            id = this.getAttribute('id')
            this.parentElement.previousSibling.innerText = this.innerText
            this.parentElement.previousSibling.setAttribute( 'id', this.getAttribute('id' ))
        }
        content_month_el.appendChild( a )
    
    }
    month_el.appendChild( btn_month_el )
    month_el.appendChild( content_month_el )
    return month_el;
}

function get_years()
{
    data = [
        {name:'2021', id: 2021},
        {name:'2022', id: 2022},
        {name:'2023', id: 2023},
        {name:'2024', id: 2024},
        {name:'2025', id: 2025},
    ]
    month_el = document.createElement( 'div' )
    month_el.classList.add('drop-list');
    month_el.classList.add('years');

    btn_month_el = document.createElement( 'div' )
    btn_month_el.classList.add('drop-list-btn');
    btn_month_el.classList.add('years');
    btn_month_el.innerText = "Год"

    content_month_el = document.createElement( 'div' )
    content_month_el.classList.add('drop-list-content');
    content_month_el.classList.add('years');
    

    btn_month_el.onclick = function()
    {
        if( this.classList.contains( '_open' ) && this.nextSibling.classList.contains( 'show' ) )
        {
            set_dtn = document.getElementsByClassName( 'drop-list-content' )
            for( let i of set_dtn )
            {
                i.classList.remove( 'show' )
                i.previousSibling.classList.remove( '_open' )
            }
            this.classList.remove( '_open' )
            this.nextSibling.classList.remove( 'show' )    
        }
        else
        {
            set_dtn = document.getElementsByClassName( 'drop-list-content' )
            for( let i of set_dtn )
            {
                i.classList.remove( 'show' )
                i.previousSibling.classList.remove( '_open' )
            }
            this.classList.add( '_open' )
            this.nextSibling.classList.add( 'show' )
        }
    }
    for( let i of data )
    {
        a = document.createElement( 'a' )
        a.setAttribute( 'id', i.id );
        a.innerText = i.name
        a.onclick = function()
        {
            id = this.getAttribute('id')
            this.parentElement.previousSibling.innerText = this.innerText
            this.parentElement.previousSibling.setAttribute( 'id', this.getAttribute('id' ))
        }
        content_month_el.appendChild( a )
    
    }
    month_el.appendChild( btn_month_el )
    month_el.appendChild( content_month_el )
    return month_el;
}

function get_months_and_input()
{
    var wrapper = document.createElement("div");
    wrapper.classList.add( "months_and_input" )

    var input = document.createElement("input");
    input.classList.add( "input" )
    input.classList.add( "input_summ" )
    input.placeholder = "Сумма"

    var add_btn = document.createElement("div");
    add_btn.classList.add( "add_btn_input" )
    add_btn.onclick = function()
    {
        document.querySelector('.months_and_input').before( get_months_and_input() )
        this.classList = 'del_btn_input'
        this.onclick = function()
        {
            this.parentElement.remove()
        }
    }

    wrapper.appendChild( get_years() )
    wrapper.appendChild( get_months() )
    
    wrapper.appendChild( input )
    wrapper.appendChild( add_btn )
    return wrapper;
}