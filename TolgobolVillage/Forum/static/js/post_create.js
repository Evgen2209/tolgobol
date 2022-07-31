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
function initpost_create()
{
    create_post = document.querySelector("#create_post")
    if( create_post )
    {
        console.log(create_post)
        create_post.onclick = function()
        {
            
            title = document.getElementById("title").value
            text = document.getElementById("text").value
            if( text && title )
            {
                data = new FormData()
                                
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
                data.append( 'section_id', this.getAttribute( 'name' ) )
                data.append( 'text', text )
                data.append( 'title', title )
                data.append( 'files', file )
                function success(data)
                {
                    console.log(data.url, text)
                    window.location.href = data.url
                }
                send_ajax( data, 'ForumService.PostCreate', success )
                //Файлы
            }
            else
            {
                //Введите текст
            }
        }


    }
}
initpost_create()
