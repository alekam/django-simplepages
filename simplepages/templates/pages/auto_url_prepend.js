function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}

var simplepages_site_sections = { {% for section in sections %}{{section.id}}: '{{section.url}}'{% if forloop.last %}{% else %},{% endif %}{% endfor %} };
addLoadEvent(function() {
    var site_select = document.getElementById('id_site_section');
    site_select.onchange = function() {
        var site_select = document.getElementById("id_site_section");
        if (site_select.value) {
            var prepend_url = false;
            var simplepage_url=document.getElementById("id_url");
            if (simplepage_url.value == "") {
                prepend_url = true;
            } else {
                // Checking to see if the url is just one of the other section urls
                // if it is go ahead and replace it
                for(section in simplepages_site_sections) {
                    if (simplepage_url.value == simplepages_site_sections[section]) {
                        prepend_url = true;
                        break;   
                    }
                }
            }
            if (prepend_url) {
                simplepage_url.value = simplepages_site_sections[site_select.value];
            }
        }
    }
});

