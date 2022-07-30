function create_text_content_modal( text )
{
  var p = document.createElement("p");
  p.className = "modal__title";
  p.innerText = text;
  return p
}

function create_img_content_modal( text )
{
  var p = document.createElement("img");
  p.setAttribute( 'href', text )
  p.setAttribute( 'src', text )
  p.className = "img_modal";
  // p.className = "modal__title";
  // p.innerText = text;
  return p
}

function create_modal( text, is_img=false )
{
  console.log(is_img, 'is_img')
  var overlay = document.createElement("dev");
  overlay.className = 'fixed-overlay';
  overlay.classList.add('fixed-overlay__modal');
  overlay.id = "overlay-modal";


  var modal = document.createElement("dev");
 

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

  if( is_img )
  {
    var p = create_img_content_modal( text );
    modal.className = 'modal_img';
  }
  else
  {
    var p = create_text_content_modal( text );
    modal.className = 'modal';
  }
  modal_container.appendChild( close_el );
  modal_container.appendChild( p );
  modal.appendChild( modal_container );
  overlay.appendChild( modal );
  document.body.classList.toggle('_lock')
  document.body.appendChild( overlay );
}
