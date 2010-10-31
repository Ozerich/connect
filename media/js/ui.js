var showed = 0;
var openedDialog;

function ui_init()
{
    var body = document.getElementsByClassName("dialog-blackout")[0];
    body.onclick = function(e){
        if(showed == 1)
            showed = 2;
        else if(showed == 2)
        {
            var x = e.clientX, y = e.clientY;
            if(x < openedDialog.offsetLeft || y < openedDialog.offsetTop || x > openedDialog.offsetLeft + openedDialog.clientWidth 
            || y > openedDialog.offsetTop + openedDialog.clientHeight)
                ui_hide_dialog(openedDialog.id);
        }
    }
}

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

function ui_show(id) {
    x = document.getElementById(id);
    x.style.display = '';
}

function ui_hide(id) {
    x = document.getElementById(id);
    x.style.display = 'none';
}

function ui_show_dialog(id) {
    ui_show(id);
    ui_center(id);
    ui_show('blackout');
    ui_fullscreen('blackout');
    openedDialog = document.getElementById(id);
    showed = 1;
}

function ui_hide_dialog(id){
    showed = 0;
    ui_hide(id);
    ui_hide('blackout');
}

function ui_fullscreen(el) {
    e = document.getElementById(el)
    sw = document.documentElement.scrollWidth;
    sh = document.documentElement.scrollHeight;
    e.style.width = sw + 'px';
    e.style.height = sh + 'px';
}
