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
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var buttons = document.getElementsByClassName("voting_send");
var i;
for (i = 0; i < buttons.length; i++)
{
  buttons[i].onclick = function() {
    btn = this;
    var id_vitung = this.name;
    var set = $('input[name="'+id_vitung+'"');
    var el_need_send = null
    var disabled = false;
    set.each( function( index, el ) 
    {
      if( el.disabled )
      {
        disabled = true;
      }
      else 
      {
        if( el.checked )
        {
          el_need_send = el
        }
      }
    }
    );
    if( disabled )
    {
        // Уже голосовали, ничего не делаем
        console.log('Уже голосовали, ничего не делаем');
    }
    else
    {
      if( !Boolean( el_need_send ) ) 
      {
        //вывести сообщение о том что нужно выбрать элимент
        create_modal( 'Пожалуйста выбирите один из вариантов' );
      }
      else
      {
        var item_id = el_need_send.id;
        var comment = $('textarea[id="'+id_vitung+'"')[0].value;
        $.ajax({
          url: '/mainservise/',
          method: 'post',
          dataType: 'html',
          dataType: 'json',
          data: {
              "voting_id": el_need_send.name,
              "voting_item_id": item_id,
              "comment": comment
          },
          headers: {
              "X-Requested-MethodName": "MainService.Voting"
          },
          beforeSend: function (xhr) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          },
          success: function(data){
            if( data.error )
            {
              create_modal( data.error );            
            }
            else
            {
              create_modal( data.success );
              btn.disabled = true;
              sleep(2000).then(() => { window.location.reload(); });
            }
          },
          error: function(er) {
              console.log(er);
          }
      });        

      }
    }

  } 
}

