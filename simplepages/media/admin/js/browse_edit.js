function django_admin_links_div() {
    // Update these variables for your site
    var admin_url = '/admin/';
    var div_title = 'Django Admin';
    var div_style = 'position: fixed; top: 0; right: 0; border: solid 1px #417690; padding: 3px 5px 3px 5px; text-align: center; color: #fff; background: #EFEFEF; font-size: 11px; z-index:999;';
    var link_color = '#417690';
    // end variables to update
    if(typeof ActiveXObject != 'undefined') {
       var x = new ActiveXObject('Microsoft.XMLHTTP');
    }
    else if(typeof XMLHttpRequest != 'undefined') {
       var x = new XMLHttpRequest();
    }
    else {
       return;
    }
    x.open('GET', location.href, false);
    x.send(null);
    try {
       var type = x.getResponseHeader('x-object-type');
       var id = x.getResponseHeader('x-object-id');
    }
    catch(e) {
       return;
    }
    var div = document.createElement('div');
    div.style.cssText = div_style;
    div.innerHTML = '<b><a href="'+admin_url+'" style="color: '+link_color+';">'+div_title+'</a></b><br /><a href="'+admin_url + type.split('.').join('/') + '/' + id + '/" style="color: '+link_color+';">Edit '+type.split('.')[1]+'</a> &nbsp; <a href="'+admin_url+'logout/" style="color: '+link_color+';">Logout</a>';
    document.body.appendChild(div);
}
django_admin_links_div();