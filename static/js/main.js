$(document).ready(function () {
    $('input[type=checkbox], input[type=radio]').each(function () {
        $(this).prettyCheckable();
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
