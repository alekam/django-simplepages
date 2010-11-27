// Finds all fieldsets with class="collapse", collapses them, and gives each
// one a "Show" link that uncollapses it. The "Show" link becomes a "Hide"
// link when the fieldset is visible.

function findForm(node) {
    // returns the node of the form containing the given node
    if (node.tagName.toLowerCase() != 'form') {
        return findForm(node.parentNode);
    }
    return node;
}

var CollapsedFieldsets = {
    collapse_re: /\bcollapse\b/,   // Class of fieldsets that should be dealt with.
    collapsed_re: /\bcollapsed\b/, // Class that fieldsets get when they're hidden.
    collapsed_class: 'collapsed',
    init: function() {
        var fieldsets = document.getElementsByTagName('fieldset');
        var collapsed_seen = false;
        for (var i = 0, fs; fs = fieldsets[i]; i++) {
            // Collapse this fieldset if it has the correct class, and if it
            // doesn't have any errors. (Collapsing shouldn't apply in the case
            // of error messages.)
            if (fs.className.match(CollapsedFieldsets.collapse_re) && !CollapsedFieldsets.fieldset_has_errors(fs)) {
                collapsed_seen = true;
                // Give it an additional class, used by CSS to hide it.
                fs.className += ' ' + CollapsedFieldsets.collapsed_class;
                if(! fs.id) {
                    fs.id = 'django-collapsing-fieldset-'+i;   
                }
                // (<a id="fieldsetcollapser3" class="collapse-toggle" href="#">Show</a>)
                var collapse_link = document.createElement('a');
                collapse_link.className = 'collapse-toggle';
                collapse_link.id = 'fieldsetcollapser' + fs.id;
                
                collapse_link.onclick = new Function('CollapsedFieldsets.show("'+fs.id+'"); return false;');
                collapse_link.href = '#';
                collapse_link.innerHTML = gettext('Show');
                var h2 = fs.getElementsByTagName('h2')[0];
                h2.appendChild(document.createTextNode(' ('));
                h2.appendChild(collapse_link);
                h2.appendChild(document.createTextNode(')'));
            }
        }
        if (collapsed_seen) {
            // Expand all collapsed fieldsets when form is submitted.
            addEvent(findForm(document.getElementsByTagName('fieldset')[0]), 'submit', function() { CollapsedFieldsets.uncollapse_all(); });
        }
    },
    fieldset_has_errors: function(fs) {
        // Returns true if any fields in the fieldset have validation errors.
        var divs = fs.getElementsByTagName('div');
        for (var i=0; i<divs.length; i++) {
            if (divs[i].className.match(/\berror\b/)) {
                return true;
            }
        }
        return false;
    },
    show: function(fieldset_id) {
        var fs = document.getElementById(fieldset_id);
        // Remove the class name that causes the "display: none".
        if (fs.className) {
            fs.className = fs.className.replace(CollapsedFieldsets.collapsed_re, '');
        }
        // Toggle the "Show" link to a "Hide" link
        var collapse_link = document.getElementById('fieldsetcollapser' + fieldset_id);
        collapse_link.onclick = new Function('CollapsedFieldsets.hide("'+fs.id+'"); return false;');
        collapse_link.innerHTML = gettext('Hide');
    },
    hide: function(fieldset_id) {
        var fs = document.getElementById(fieldset_id);
        // Add the class name that causes the "display: none".
        fs.className += ' ' + CollapsedFieldsets.collapsed_class;
        // Toggle the "Hide" link to a "Show" link
        var collapse_link = document.getElementById('fieldsetcollapser' + fieldset_id);
        collapse_link.onclick = new Function('CollapsedFieldsets.show("'+fs.id+'"); return false;');
        collapse_link.innerHTML = gettext('Show');
    },

    uncollapse_all: function() {
        var fieldsets = document.getElementsByTagName('fieldset');
        for (var i=0; i<fieldsets.length; i++) {
            if (fieldsets[i].className.match(CollapsedFieldsets.collapsed_re)) {
                CollapsedFieldsets.show(fieldsets[i].id);
            }
        }
    }
};

addEvent(window, 'load', CollapsedFieldsets.init);