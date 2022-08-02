
function create_modal_insert( id )
{
    var wrapper_modal = document.createElement("div");
    wrapper_modal.setAttribute('id', id)
    var p = document.createElement("p");
    p.className = "modal__title";
    p.innerText = "Укажите адрес";

    var btn = document.createElement("button");
    btn.className = "button";
    btn.innerText = "Внести";
    btn.onclick = function()
    {
        insert_list = []
        el_list = document.getElementsByClassName('months_and_input')
        for( let i of el_list )
        {
            buf = {
                year: i.querySelector( '.drop-list-btn.years' ).getAttribute('id'),
                months: i.querySelector( '.drop-list-btn.months' ).getAttribute('id'),
                summ: i.querySelector( '.input_summ' ).value,
            }
            insert_list.push(buf)
        }
        data = {
            collect_id: wrapper_modal.getAttribute('id'),
            insert_list: JSON.stringify( insert_list ),
            adres_id: document.querySelector('.modal_container').querySelector('.adress').getAttribute('name')
        }
        send_ajax( '/mainservise/', data, 'MainService.InsertCollectOnMonths', function(data){
            document.getElementById('overlay-modal').remove()
        } )
    }

    wrapper_modal.appendChild( p )
    wrapper_modal.appendChild( create_adres_component() )
    wrapper_modal.appendChild( get_months_and_input() )
    wrapper_modal.appendChild( btn )
    create_modal( wrapper_modal )

}


function collect_btn_on_months()
{
    create_modal_insert( this.getAttribute('id') )
}

function collect_btn_on()
{
    console.log( this.getAttribute('months'),22222222 )
}

function init_collect_btn()
{
    btns = document.getElementsByClassName( 'insert_collect_btn' )
    for( let item of btns )
    {
        
        if( Number( item.getAttribute('months') ) )
        {
            // по месячно
            item.onclick = collect_btn_on_months
        }
        else
        {
            item.onclick = collect_btn_on
            
        }
    }
}

init_collect_btn()



