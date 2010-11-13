
function ui_center_el(e) {
    sw = window.innerWidth;
    sh = window.innerHeight;
    e.style.left = (sw / 2 - e.clientWidth / 2) + 'px';
    e.style.top = (sh / 2 - e.clientHeight / 2) + 'px';
    if (sh < e.clientHeight)
        e.style.top = '0px';
}

function ui_center(el) {
    ui_center_el(document.getElementById(el));
}

function ui_show_dialog(id) {
    $('#'+id).fadeTo("normal", 1);
    $('#blackout').fadeTo("normal", 1);
    $('#blackout').click(function() {
        $('#'+id).fadeTo("normal", 0);
        $('#blackout').fadeTo("normal", 0, function() {
            $('#blackout').hide();
            $('textarea').val('');
            $('#error_dialog_div').css('display','none');
            $('.dialog input[type="text"]').val('');
            $('.dialog input[type="file"]').val('');
            var a = 1;
        });      
        
    });
    ui_center(id);
    ui_fullscreen('blackout');
}


function ui_fullscreen(el) {
    e = document.getElementById(el)
    sw = document.documentElement.scrollWidth;
    sh = document.documentElement.scrollHeight;
    e.style.width = sw + 'px';
    e.style.height = sh + 'px';
}

function ui_show_user_info(evnt, n, f) {
    e = document.getElementById('user-info-popup');
	if (!evnt)
		evnt = window.event;
    e.style.left = (evnt.clientX + window.pageXOffset + 10) + 'px';
    e.style.top = (evnt.clientY + window.pageYOffset + 10) + 'px'; 
    $('#user-info-popup').stop().fadeTo('normal', 1);
    document.getElementById('user-info-name').innerHTML = n;
    document.getElementById('user-info-fac').innerHTML = f;
}

function ui_hide_user_info(n, f) {
    $('#user-info-popup').stop().fadeOut();
}

function ui_show_comment_form(where, reply) {
    document.getElementById(where).innerHTML = replyFormHTML;
    document.getElementById('reply-to').value = reply;
}

function attach_file(id) {
    f = $('#file-template-'+id).clone();
    f.css('display', '');
    f.appendTo('#attach-preview');
}

function detach_file(id) {
    $('#file-template-'+id+':first').detach();
}

function check_sendmsg_form()
{
    var error_div = $('#error_div');
    if($('#text').val() == "" && document.getElementById('attach-preview').childNodes.length == 0)
    {
        error_div.css('display','block');
        error_div.html('Cообщение не может быть пустым');
        return false;
    }
    else
    {
        error_div.css('display','none');
        return true;
    }
}

function check_addtopic_form()
{
    var error_div = $('#error_dialog_div');
    if($('#header').val() == "")
    {
        error_div.css('display','block');
        error_div.html('Заголовок темы не может быть пустым');
        return false;
    }
    else
    {
        error_div.css('display','none');
        return true;
    }
}

function check_addevent_form()
{
    var error_div = $('#error_dialog_div');
    if($('#event_name').val() == "")
    {
        error_div.css('display','block');
        error_div.html('Событие не может быть пустым');
        return false;
    }
    else if($('#datepicker').val() == "")
    {
        error_div.css('display','block');
        error_div.html('Не указана дата события');
        return false;
    }
    else
    {
        error_div.css('display','none');
        return true;
    }
}

function check_addfile_form()
{
    var error_div = $('#error_dialog_div');
    if($('#file').val() == "")
    {
        error_div.css('display','block');
        error_div.html('Не указан загружаемый файл');
        return false;
    }
    else
    {
        error_div.css('display','none');
        return true;
    }
}
