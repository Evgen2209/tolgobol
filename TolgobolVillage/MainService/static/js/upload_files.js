class FileUpload {
    constructor(input, item) {
        this.input = input
        this.max_length = 1024 * 1024 * 1; // 10 mb
        this.item = item
        this.progres_current = item.querySelector( '.progres_current' )
    }

    upload() {
        // this.create_progress_bar();
        this.initFileUpload();
    }

    initFileUpload() {
        this.file = this.input.files[0];
        // this.upload_file(0, null);
        this.start_upload();
    }

    start_upload()
    {
        if( !Boolean(this.file) ) return;
        var self = this;
        console.log( this.file.name )
        console.log( this.file.size )
        var formData = new FormData();
        formData.append('size', this.file.size);
        formData.append('file_name', this.file.name);

        $.ajax({
            url: '/upload/',
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
            headers: {
                "X-Requested-MethodName": "UploadingFiles.StartUpload",
                "X-CSRFToken": get_csrftoken()
            },    
            error: function (data) {
                console.log( 'ERROR ', data );
                $(self.progres_current).css('background-color', '#f74646')
            },
            success: function (data) {
                if( data.success )
                {
                    self.item.setAttribute( 'name', data.success )
                    self.upload_file( 0, data.success )
                }
                else
                {
                    console.log( 'ERROR ', data.error );
                }
            }
        });
    }

    upload_file(start, path) {
        if( !Boolean(this.file) ) return;
        var end;
        var self = this;
        var tmp_name = path;
        var formData = new FormData();
        var nextChunk = start + this.max_length + 1;
        var currentChunk = this.file.slice(start, nextChunk);
        var uploadedChunk = start + currentChunk.size
        if( self.item.getAttribute( 'del' ) )
        {
            return;
        }
        if (uploadedChunk >= this.file.size) {
            end = 1;
        } else {
            end = 0;
        }
        formData.append('file', currentChunk);
        formData.append('tmp_name', tmp_name);
        formData.append('chunk_size', nextChunk);

        $.ajax({
            xhr: function () {
                var xhr = new XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        if (self.file.size < self.max_length) {
                            var percent = Math.round((e.loaded / e.total) * 100);
                        } else {
                            var percent = Math.round((uploadedChunk / self.file.size) * 100);
                        }
                        $(self.progres_current).css('width', percent + '%')
                    }
                });
                return xhr;
            },
            url: '/upload/',
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
            headers: {
                "X-Requested-MethodName": "UploadingFiles.Upload",
                "X-CSRFToken": get_csrftoken()
            },    
            error: function (xhr) {
                console.log(xhr);
                $(self.progres_current).css('background-color', '#f74646')
            },
            success: function (res) {
                if (nextChunk < self.file.size) {
                    tmp_name = res.success
                    self.upload_file(nextChunk, tmp_name);
                } else {
                    // Загрузка заверще
                    $(self.progres_current).css('background-color', '#0ebf0e')
                    // self.item.querySelector(".file_item_del").classList.add("show")
                    console.log(res.success,'res.success')
                    var formData = new FormData();
                    formData.append( 'tmp_name', res.success )
                    $.ajax({
                        url: '/upload/',
                        type: 'POST',
                        dataType: 'json',
                        cache: false,
                        processData: false,
                        contentType: false,
                        data: formData,
                        headers: {
                            "X-Requested-MethodName": "UploadingFiles.FinishUpload",
                            "X-CSRFToken": get_csrftoken()
                        },    
                        error: function (xhr) {
                        },
                        success: function (res) {
                            self.item.setAttribute( 'id', res.success )
                        }
                    });
                }
            }
        });
    };
}



document.querySelector( '.main_input_file' ).addEventListener('change',function(e) {

})
function init_upload_form()
{
    form = document.querySelector( '.main_input_file' )
    if( !form ) return;
    form.addEventListener('change',function(e) {
    //Если форма изменилась то начинаем загрузку
    e.preventDefault();
    var f_name = [];

    //Добавление имени файла  который быбрали в поле что бы пользователь видел
    for(var i = 0; i < $(this).get(0).files.length; ++i) {

        f_name.push($(this).get(0).files[i].name);

    }
    if( f_name.length == 0 ) return;
    progres_item = document.createElement('div')
    progres_item.classList.add('progres_item')

    input_wrapper = document.createElement('div')
    input_wrapper.classList.add('input_wrapper')

    input = document.createElement('input')
    input.classList.add('f_name')
    input.setAttribute( 'type', "text" )
    input.setAttribute( 'id', "f_name" )
    input.setAttribute( 'disabled', true )

    progres_base = document.createElement('div')
    progres_base.classList.add('progres_base')

    progres_current = document.createElement('div')
    progres_current.classList.add('progres_current')
    progres_current.style.width = '0%'

    btn_del = document.createElement('div')
    btn_del.classList.add('file_item_del')
    btn_del.onclick = function()
    {
        this.closest('.progres_item').setAttribute('del', true)
        var data_del = new FormData();
        data_del.append('tmp_name', this.closest('.progres_item').getAttribute('name'));
        $.ajax({
            url: '/upload/',
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: data_del,
            headers: {
                "X-Requested-MethodName": "UploadingFiles.CancelUpload",
                "X-CSRFToken": get_csrftoken()
            },    
            error: function (xhr) {
                console.log(xhr);
            },
            success: function (res) {
            }
        });
        this.closest('.progres_item').remove()

    }
    input_wrapper.appendChild( input )
    input_wrapper.appendChild( btn_del )
    progres_base.appendChild( progres_current )
    progres_item.appendChild( input_wrapper )
    progres_item.appendChild( progres_base )
    // progres_item.appendChild( btn_del )

    $(input).val(f_name.join(", "));
    progres_wrapper = document.querySelector('.progres_wrapper')
    progres_wrapper.appendChild( progres_item )

    var uploader = new FileUpload( e.target, progres_item )
    uploader.upload();
    } )
}
init_upload_form()