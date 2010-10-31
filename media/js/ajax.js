function ajax(URL, ajaxHandler)
{
	xmlReq = null;
	if (window.XMLHttpRequest) xmlReq = new XMLHttpRequest();
    	else if(window.ActiveXObject) xmlReq = new ActiveXObject("Microsoft.XMLHTTP");
	if (xmlReq == null) return;
	xmlReq.onreadystatechange = function()
	{
		if (xmlReq.readyState == 4)
			ajaxHandler(xmlReq.responseText);
	}
	xmlReq.open ('GET', URL, true);
	xmlReq.send (null);
    return false;
}

function ajaxLoadMessages(id, start) {
    ajax("/messages/view/" + id + "?ajax=" + start,
        function(html) {
            document.getElementById("messages").innerHTML += html;
            document.getElementById("ajaxLoadBtn").onclick = 
                function() {
                    ajaxLoadMessages(id, start+10);
                } 
            if (html.length == 0)
                document.getElementById("ajaxLoadBtn").style.display = 'none';
        });
}
