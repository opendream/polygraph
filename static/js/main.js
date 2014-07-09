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
      
      $('#' + $(this).attr('target')).load($(this).attr('href'));
      
    });

    var resize_input = function () {
        $(this).attr('size', $(this).val().length+1);
    };
    $('.tagit-new input[type="text"]').keyup(resize_input).each(resize_input);


    // confirm delete
    $('.btn-delete').popConfirm({
        title: "Delete Item",
        content: "Are you sure you want to delete this item?",
        placement: "top"
    });

    // load more inline
    var found_current_revision = false;
    var ilm_length = $('.load-more-inline-wrapper li').length

    $('.load-more-inline-wrapper li').each(function (i, item) {

        if (i > 4 && found_current_revision) {
            $(this).addClass('hidden');
        }

        if ($(this).hasClass('current-revision')) {
            found_current_revision = true;
            if (i+1 == ilm_length) {
                $('.load-more-inline').remove();
            }
        }

    });

    $('.load-more-inline').click(function (e) {
        e.preventDefault();
        $($(this).attr('href')).find('li').removeClass('hidden');
        $(this).remove();
    });

    // front tab
    $('.tabable').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    });
    $('.first .tabable').tab('show')

    $('.dropdown-menu').on('click', 'li a', function(){
        $('#meter-tab-drop .text').text($(this).text());
    });

});

/*
$(window).on('scroll', function() {

    var offset = $(this).scrollTop();

    $('.cke_inner > .cke_top').each(function () {

        var tool = $(this);
        var inner = tool.parent();
        var toolOffset = tool.offset().top;
        var toolwidth = inner.width();
        var toolheight = tool.height();

        var nav_fixed_height = $('.navbar-fixed-top').height();


        console.log('offset', offset+ $('.navbar-fixed-top').height() );
        console.log('toolOffset', toolOffset);
        console.log('nav_fixed_height', nav_fixed_height);

        if (offset + nav_fixed_height > toolOffset && tool.css('position') != 'fixed') {
            inner.css({'padding-top': toolheight});
            tool.css({
                position: 'fixed',
                top: nav_fixed_height,
                width: toolwidth,
                'z-index': 1000000
            });
        }
        else {
            inner.css({'padding-top': 0});
            tool.css({
                position: 'static',
                top: nav_fixed_height,
                width: 'auto'
            });
        }
    });

});
*/

/*
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
*/