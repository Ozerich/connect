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
	if(!evnt)
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
