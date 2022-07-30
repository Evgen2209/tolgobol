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

function hight_btn()
{
    btn = document.getElementById( "hight_btn" )
    panel = document.getElementById( "output_panel" )
    panel.classList.toggle( "open_panel" )
    if( btn.innerText == "Свернуть" )
    {
        btn.innerText = "Развернуть"
        ara = document.querySelector('.message_area')
        ara.classList.toggle('message_hight')
    }
    else {
        btn.innerText = "Свернуть"
        ara = document.querySelector('.message_area')
        ara.classList.toggle('message_hight')

    }
}

function init_hight_btn()
{
    btn = document.getElementById( "hight_btn" )
    if( btn )
    {
        btn.onclick = hight_btn
    }

}
init_hight_btn()

function respons_btn()
{
    btns = document.getElementsByClassName( "btn_message_answer" )
    for( let item of btns )
    {
        item.onclick = function()
        {
            div = document.getElementById( item.getAttribute('name') )
            text_el = div.querySelector( '.post_text' )
            post_author_el = div.querySelector( '.post_author' )
            post_data_el = div.querySelector( '.post_data' )
            respons_message = document.createElement( 'div' )
            respons_message.classList.add( 'respons_message' )
            respons_message.classList.add( 'parent_text' )

            perent_wrapper = document.createElement( 'div' )
            perent_wrapper.classList.add( 'perent_wrapper' )

            parent_text = document.createElement( 'div' )
            parent_text.classList.add( 'parent_text' )
            text = text_el.innerText
            if( text.length > 100 )
            {
                text = text.slice( 0, 100 ) + '...'
            }
            parent_text.innerText = text

            parent_meta = document.createElement( 'div' )
            parent_meta.classList.add( 'parent_meta' )

            post_author = document.createElement( 'div' )
            post_author.classList.add( 'post_author' )
            post_author.innerText = post_author_el.innerText

            post_data = document.createElement( 'div' )
            post_data.classList.add( 'post_data' )
            post_data.innerText = post_data_el.innerText
            delet_parent_sms = document.createElement( 'a' )
            delet_parent_sms.classList.add( 'delet_parent_sms' )
            delet_parent_sms.innerText = 'Открепить'
            delet_parent_sms.onclick = function()
            {
                respons_message.remove()
            }
            parent_meta.appendChild( post_author )
            parent_meta.appendChild( post_data )
            perent_wrapper.appendChild( parent_text )
            perent_wrapper.appendChild( parent_meta )

            respons_message.appendChild( perent_wrapper )
            respons_message.appendChild( delet_parent_sms ) 
            respons_message.setAttribute('id', item.getAttribute('name'))
            buf = output_panel.querySelector( '.respons_message' )
            if( buf )
            {
                buf.remove()
            }
            output_panel.prepend( respons_message )
            panel = document.getElementById( "output_panel" )
            if( panel.classList.contains( "open_panel" ) )
            {
                
            }
            else{
                hight_btn() 
            }
    //   <div class="respons_message parent_text">
        //     <div class="perent_wrapper">
        //       <div class="parent_text">
        //         inventore quod aliquam similique blanditiis assumenda sequi eveniet id, qui voluptate ea corrupti expedita culpa cum sed!
        //       </div>
        //       <div class="parent_meta">
        //         <div class="post_author">Автор</div>
        //         <div class="post_data">Дата</div>
        //       </div>
        //     </div>
        //     <a href="" class="delet_parent_sms">Открепить</a>
        //   </div>
  
        }
    }
}
respons_btn()
function success_send_message( data )
{
    if( data.success )
    {
        window.location.reload()
        document.querySelector('.message_area').scrollHeight
    }
    if( data.error )
    {
        console.log( data.error )
    }
    else
    {
        console.log( 'Не предвиденный ответ ', data )
    }
}

function send_ajax( data, method_name, func_success )
{
    $.ajax( {
        url: '/forum/forumservice/',
        type: 'POST',
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        data: data,
        // запрос на список квартир
        headers: {
            "X-Requested-MethodName": method_name
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: func_success,
        error: function(er)
        {
            console.log( er );
        }
    } )

}

function send_message()
{
    panel = document.getElementById( 'output_panel' )
    text = panel.querySelector( 'textarea' ).value
    if( text )
    {
        data = new FormData()
        
        respons_el = panel.querySelector( '.respons_message' )
        if( respons_el )
        {
            data.append( 'related_message', respons_el.getAttribute( 'id' ) )
        }
        
        files_el = document.getElementsByClassName('progres_item')
        file = []
        for( let el of files_el )
        {
            id = el.getAttribute('id')
            if( id )
            {
                file.push( el.getAttribute('id') )
            }
            
        }
        data.append( 'post', document.getElementById( 'post_wrapper' ).getAttribute( 'name' ) )
        data.append( 'text', text )
        data.append( 'files', file )
        send_ajax( data, 'ForumService.SendMessage', success_send_message )
        //Файлы
    }
    else
    {
        //Введите текст
    }
   
}

function init_send_message()
{
    btn = document.getElementById( 'send_message' )
    if( btn )
    {
        btn.onclick = send_message
    }
}

init_send_message()

function update_btn()
{
    btn = this
    block = this.parentElement.parentElement.parentElement
    
    text_el = block.querySelector( 'p' )
    post = text_el.parentElement
    area = document.createElement('textarea')
    area.classList.add('output_message')
    area.value = text_el.innerText  
    // прячим родной текст и кнопку
    text_el.classList.toggle('hide')
    this.classList.toggle('hide')

    save = document.createElement( 'a' )
    save.classList.add( 'btn_message' )
    save.classList.add( 'btn_message_update' )
    save.innerText = "Сохранить"
    save.onclick = function()
    {
        
        date = {}
        date.text = area.value
        date.post = post.getAttribute('id')
        date.author = post.querySelector( '.post_meta' ).querySelector( '.post_author' ).getAttribute('name')
        func_success = function()
        {
            text_el.innerText = date.text
            area.remove()
            save.remove()
            cancel.remove()
            btn.classList.toggle('hide')
            text_el.classList.toggle('hide')    
        }
        send_ajax( date, 'ForumService.UpdateMessage', func_success )
    }

    cancel = document.createElement( 'a' )
    cancel.classList.add( 'btn_message' )
    cancel.classList.add( 'btn_message_update' )
    cancel.innerText = "Отменить"
    cancel.onclick = function()
    {
        area.remove()
        save.remove()
        cancel.remove()
        btn.classList.toggle('hide')
        text_el.classList.toggle('hide')
        
    }
    post.prepend( area )
    this.parentElement.appendChild( save )
    this.parentElement.appendChild( cancel )

}

function init_update_btn()
{
    btns = document.getElementsByClassName( "btn_message_update" )
    for( let item of btns )
    {
        item.onclick = update_btn
    }

}

init_update_btn()


function delet_btn()
{
    post = this.parentElement.parentElement.parentElement
    data = {}
    data.post_id = post.querySelector( '.post_self' ).getAttribute( 'id' )
    data.author = post.querySelector('#post_meta_self').querySelector('.post_author').getAttribute( 'name' )
    func_success = function()
    {
        post.remove()
    }
    send_ajax( data, 'ForumService.DeletMessage', func_success )
}

function init_delet_btn()
{
    btns = document.getElementsByClassName( "btn_message_delet" )
    for( let item of btns )
    {
        item.onclick = delet_btn
    }

}

init_delet_btn()

function img_btn()
{
    create_modal( this.getAttribute( 'id' ), true )
}

function init_img_btn()
{
    btns = document.getElementsByName( "img_btn" )
    for( let item of btns )
    {
        item.onclick = img_btn
    }

}
init_img_btn()