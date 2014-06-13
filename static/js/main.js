function cloneMore(selector, type) {

    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}

$(document).ready(function () {
    // checknox radio style
    $('input[type=checkbox], input[type=radio]').each(function () {
        $(this).prettyCheckable();
    });

    // add more formset
    $('.add_more').click(function() {


        var selector = '#' + $(this).attr('id').replace('_add_more', '');
        var type = selector.replace('#id_', '')

        selector = selector + '>:last'

        var newElement = $(selector).clone(true);
        var total = $('#id_' + type + '-TOTAL_FORMS').val();
        newElement.find(':input').each(function() {
            var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newElement.find('label').each(function() {
            var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
            $(this).attr('for', newFor);
        });
        total++;
        $('#id_' + type + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);

    });

    // popup create link
    $('.popup-create-link, .popup-edit-link').click(function (e) {
        e.preventDefault();

        var wkey = $(this).attr('href').replace('/', '');

        window.open($(this).attr('href') + '?_popup=1', wkey, "width=auto,height=auto");

    });
    
    $(document).on('click', '.add-another-inline', function (e) {
      e.preventDefault();
      
      var href = $(this).attr('href');
      console.log(href);
      
      $('#' + $(this).attr('target')).load($(this).attr('href'));
      
    });

});

if (typeof CKEDITOR != 'undefined') {
    CKEDITOR.on('dialogDefinition', function(ev) {
        // Take the dialog window name and its definition from the event data.
        var dialogName = ev.data.name;
        var dialogDefinition = ev.data.definition;

        if (dialogName == 'image') {
            dialogDefinition.onShow = function () {
                // This code will open the Upload tab.
                this.selectPage('Upload');
            };
        }
    });
}
