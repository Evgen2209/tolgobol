$( document ).ready( function() {
  $( '.header__burger' ).click( function( event ) {
    $( '.header__burger, .menu__body' ).toggleClass( 'active' );
    $( 'body' ).toggleClass( '_lock' );
  });
});


$(".menu__arrow").click(function() {
    $(this).toggleClass("_open");
});
const isMobile = {
  Android: function() {
    return navigator.userAgent.match( /Android/i );
  },
  Blackberry: function() {
    return navigator.userAgent.match( /Blackberry/i );
  }, 
  IOS: function() {
    return navigator.userAgent.match( /iPhone|iPad|iPod/i );
  }, 

  Opera: function() {
    return navigator.userAgent.match( /Opera Mini/i );
  }, 

  Windows: function() {
    return navigator.userAgent.match( /IEMobile/i );
  }, 

  any: function() {
    return (
      isMobile.Android() ||
      isMobile.Blackberry() ||
      isMobile.IOS() ||
      isMobile.Opera() ||
      isMobile.Windows() 
    );
  }, 
};
if( isMobile.any() )
{
  document.body.classList.add( '_touch' );
  let menuArrows = document.querySelectorAll( '.menu__arrow' );
  if( menuArrows.length > 0 )
  {
    for( let index = 0; index < menuArrows.length; index++ )
    {
      const menuArrow = menuArrows[index];
      menuArrow.addEventListener( "click", function(e) {
        menuArrow.parentElement.classList.toggle( "_open" );
      });
    }
  }
}
else
{
  document.body.classList.add( '_pc' );
}

const burger = document.querySelector( '.header__burger' );
if( burger )
{
  const menuBody = document.querySelector( '.menu__body' );
  menuBody.addEventListener( "click", function(e) {
    document.body.classList.toggle( '_lock' );
    menuBody.classList.toggle( 'active' );
    burger.classList.toggle( 'active' );
  });
}