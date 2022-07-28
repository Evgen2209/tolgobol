// сворачиваем раскрывающий список если выбран элимент месяца
window.addEventListener( 'click', function(e){
    parent = e.target.parentElement
    if( e.target )
    {
        if( !e.target.classList.contains('drop-list-btn'))
        {
            set_dtn = document.getElementsByClassName( 'drop-list-content' )
            for( let i of set_dtn )
            {
                i.classList.remove( 'show' )
                i.previousSibling.classList.remove( '_open' )
            }
        }
    }
} )
function create_adres_component()
{
    refrash_adres = function() 
    {
        data = {}
        strit_id = drop_list_strit.getAttribute( 'name' );
        houss = drop_list_house.getAttribute('name');
        gous_el = drop_list_kv.getAttribute('name');

        data.strit_id = strit_id
        data.hous = houss
        qweri = 'strit_id='+strit_id + '&hous=' + houss;
        if( gous_el )
        {
            data.kv = gous_el
        }
        send_ajax( '/auth/authservice/', data, 'AuthService.GetAdres', function(data)
        {
            if( data.error ) {
                console.log( data.error );
                return;
            }
            data_adres_all = data.adres
            if( data_adres_all.length == 1 )
            {
                adres.setAttribute( 'name', data_adres_all[0].id )
            }
            else
            {
                adres.removeAttribute( 'name' )
            }
        } )
    }

    var adres = document.createElement("dev");
    adres.classList.add('adress');
    adres.id = "adres";

    var strit = document.createElement("dev");
    strit.classList.add('drop-list');
    strit.classList.add('strit');
    var drop_list_strit = document.createElement("dev");
    drop_list_strit.classList.add('drop-list-btn');
    drop_list_strit.id = "strit_id"
    drop_list_strit.innerText = "Улица"
    var drop_list_content_strit = document.createElement("dev");
    drop_list_content_strit.classList.add('drop-list-content');
    drop_list_content_strit.classList.add('strit');
    drop_list_content_strit.id = "drop_list_content_strit"
    drop_list_strit.onclick = function () {
        //прячем все выпадающие списки
        drop_list_content_strit.classList.toggle( "show" )
        drop_list_content_house.classList.remove( "show" )
        drop_list_strit.classList.toggle( "_open" )
        drop_list_house.classList.remove( "_open" )
        drop_list_content_kv.classList.remove("show");
        drop_list_kv.classList.remove("_open");

    }
    strit.appendChild( drop_list_strit )
    strit.appendChild( drop_list_content_strit )

    var house = document.createElement("dev");
    house.classList.add('drop-list');
    house.classList.add('house');
    var drop_list_house = document.createElement("dev");
    drop_list_house.classList.add('drop-list-btn');
    drop_list_house.id = "hous_id"
    drop_list_house.innerText = "Дом"
    var drop_list_content_house = document.createElement("dev");
    drop_list_content_house.classList.add('drop-list-content');
    drop_list_content_house.classList.add('house');
    drop_list_content_house.id = "drop_list_content_house"
    drop_list_house.onclick = function () {
        drop_list_content_strit.classList.remove( "show" )
        drop_list_content_house.classList.toggle( "show" )
        drop_list_strit.classList.remove( "_open" )
        drop_list_house.classList.toggle( "_open" )
        drop_list_content_kv.classList.remove("show");
        drop_list_kv.classList.remove("_open");

    }
    house.appendChild( drop_list_house )
    house.appendChild( drop_list_content_house )

    var kv = document.createElement("dev");
    kv.classList.add('drop-list');
    kv.classList.add('kv');
    var drop_list_kv = document.createElement("dev");
    drop_list_kv.classList.add('drop-list-btn');
    drop_list_kv.id = "kv_id"
    drop_list_kv.innerText = "Кв"
    var drop_list_content_kv = document.createElement("dev");
    drop_list_content_kv.classList.add('drop-list-content');
    drop_list_content_kv.classList.add('house');
    drop_list_content_kv.id = "drop_list_content_kv"

    drop_list_kv.onclick = function () {
        drop_list_content_strit.classList.remove( "show" )
        drop_list_content_house.classList.remove( "show" )
        drop_list_strit.classList.remove( "_open" )
        drop_list_house.classList.remove( "_open" )
        drop_list_content_kv.classList.toggle("show");
        drop_list_kv.classList.toggle("_open");

    }
    kv.appendChild( drop_list_kv )
    kv.appendChild( drop_list_content_kv )

    init_strit = function(data)
    {
        data_strits = data.strits
        for( i in data_strits )
        {
            // генерация а для списка улиц
            var st = document.createElement("a");
            st.id = data_strits[i].id
            st.innerText = data_strits[i].strit
            st.onclick = function()
            {
                //функция при выборе улицы
                a = this.getAttribute('id')
                drop_list_strit.setAttribute('name', a );
                drop_list_strit.innerHTML  = this.innerText;
            
                send_ajax( '/auth/authservice/', {strit_id: this.getAttribute('id')}, 'AuthService.GetAdres', function(data)
                {
                    
                    drop_list_content_house.innerHTML = '';
                    if( data.error ) {
                        console.log( data.error );
                        return;
                    }
                    data_adres_strit = data.adres
                    for ( var key in data_adres_strit ) 
                    {
                        var a = document.createElement("a");
                        a.setAttribute( 'id', data_adres_strit[key].id )
                        a.innerText = data_adres_strit[key].hous
                        a.onclick = function()
                        {
                            // a элимент дома и функция при выборе
                            drop_list_house.setAttribute('name',  this.innerText) 
                            drop_list_house.innerHTML  = this.innerText;
                            drop_list_kv.removeAttribute('name');
                            drop_list_kv.innerHTML = 'Кв'
                            drop_list_content_kv.innerHTML = ''
                            send_ajax( '/auth/authservice/', {strit_id: drop_list_strit.getAttribute('name'), hous: this.innerText}, 'AuthService.GetAdres', function(data)
                            {
                                drop_list_content_kv.innerHTML = '';
                                if( data.error ) 
                                {
                                    console.log( data.error );
                                    return;
                                }
                                data_adres_kv = data.adres
                                if( data_adres_kv.length == 1 )
                                {
                                    var aa = document.createElement('a')
                                    aa.innerText = 'нет'
                                    aa.onclick = function()
                                    {
                                        //функция выбора кв
                                        drop_list_kv.setAttribute('name',  this.text)
                                        drop_list_kv.innerHTML  = this.text;
                                        drop_list_content_kv.classList.toggle("show")
                                        drop_list_kv.classList.toggle("_open");                
                                    }
                                    drop_list_content_kv.appendChild( aa );
                                    refrash_adres();
                                }
                                else
                                {
                                    for ( var key in data_adres_kv ) 
                                    {
                                        var el_a = document.createElement('a')
                                        el_a.innerHTML = data_adres_kv[key].kv
                                        el_a.setAttribute( 'id', data_adres_kv[key].id )
                                        el_a.onclick = function()
                                        {
                                            //функция выбора кв
                                            drop_list_kv.setAttribute('name',  this.text)
                                            drop_list_kv.innerHTML  = this.text;
                                            refrash_adres();   
                                            drop_list_content_kv.classList.toggle("show")
                                            drop_list_kv.classList.toggle("_open");                
                                                 
                                        }
                                        drop_list_content_kv.appendChild( el_a );
                                    }
                                }
                            } )
                            refrash_adres()
                            drop_list_content_house.classList.toggle("show")
                            drop_list_house.classList.toggle("_open");                
                        }
                        drop_list_content_house.appendChild( a );
                    }
                } )
                drop_list_content_strit.classList.toggle("show")
                drop_list_strit.classList.toggle("_open");    
            }
            drop_list_content_strit.appendChild( st )
        }
    }
    send_ajax( '/auth/authservice/', {}, 'AuthService.GetStrit', init_strit )



    
    

    
    adres.appendChild( strit )
    adres.appendChild( house )
    adres.appendChild( kv )
    return adres;
}
