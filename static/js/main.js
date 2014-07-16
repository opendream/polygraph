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



function url_slug(s, opt) {
	s = String(s);
	opt = Object(opt);

	var defaults = {
		'delimiter': '-',
		'limit': undefined,
		'lowercase': true,
		'replacements': {},
		'transliterate': (typeof(XRegExp) === 'undefined') ? true : false
	};

	// Merge options
	for (var k in defaults) {
		if (!opt.hasOwnProperty(k)) {
			opt[k] = defaults[k];
		}
	}

	var char_map = {
		// Latin
		'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'Ç': 'C',
		'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
		'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ő': 'O',
		'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ű': 'U', 'Ý': 'Y', 'Þ': 'TH',
		'ß': 'ss',
		'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c',
		'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
		'ð': 'd', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ő': 'o',
		'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ű': 'u', 'ý': 'y', 'þ': 'th',
		'ÿ': 'y',

		// Latin symbols
		'©': '(c)',

		// Greek
		'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Θ': '8',
		'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': '3', 'Ο': 'O', 'Π': 'P',
		'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y', 'Φ': 'F', 'Χ': 'X', 'Ψ': 'PS', 'Ω': 'W',
		'Ά': 'A', 'Έ': 'E', 'Ί': 'I', 'Ό': 'O', 'Ύ': 'Y', 'Ή': 'H', 'Ώ': 'W', 'Ϊ': 'I',
		'Ϋ': 'Y',
		'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'h', 'θ': '8',
		'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': '3', 'ο': 'o', 'π': 'p',
		'ρ': 'r', 'σ': 's', 'τ': 't', 'υ': 'y', 'φ': 'f', 'χ': 'x', 'ψ': 'ps', 'ω': 'w',
		'ά': 'a', 'έ': 'e', 'ί': 'i', 'ό': 'o', 'ύ': 'y', 'ή': 'h', 'ώ': 'w', 'ς': 's',
		'ϊ': 'i', 'ΰ': 'y', 'ϋ': 'y', 'ΐ': 'i',

		// Turkish
		'Ş': 'S', 'İ': 'I', 'Ç': 'C', 'Ü': 'U', 'Ö': 'O', 'Ğ': 'G',
		'ş': 's', 'ı': 'i', 'ç': 'c', 'ü': 'u', 'ö': 'o', 'ğ': 'g',

		// Russian
		'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
		'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
		'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C',
		'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sh', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu',
		'Я': 'Ya',
		'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
		'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
		'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
		'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
		'я': 'ya',

		// Ukrainian
		'Є': 'Ye', 'І': 'I', 'Ї': 'Yi', 'Ґ': 'G',
		'є': 'ye', 'і': 'i', 'ї': 'yi', 'ґ': 'g',

		// Czech
		'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'Ň': 'N', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ů': 'U',
		'Ž': 'Z',
		'č': 'c', 'ď': 'd', 'ě': 'e', 'ň': 'n', 'ř': 'r', 'š': 's', 'ť': 't', 'ů': 'u',
		'ž': 'z',

		// Polish
		'Ą': 'A', 'Ć': 'C', 'Ę': 'e', 'Ł': 'L', 'Ń': 'N', 'Ó': 'o', 'Ś': 'S', 'Ź': 'Z',
		'Ż': 'Z',
		'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z',
		'ż': 'z',

		// Latvian
		'Ā': 'A', 'Č': 'C', 'Ē': 'E', 'Ģ': 'G', 'Ī': 'i', 'Ķ': 'k', 'Ļ': 'L', 'Ņ': 'N',
		'Š': 'S', 'Ū': 'u', 'Ž': 'Z',
		'ā': 'a', 'č': 'c', 'ē': 'e', 'ģ': 'g', 'ī': 'i', 'ķ': 'k', 'ļ': 'l', 'ņ': 'n',
		'š': 's', 'ū': 'u', 'ž': 'z',

        // Thai
        // http://en.wikipedia.org/wiki/Royal_Thai_General_System_of_Transcription
        'ก': 'k',
        'ข': 'k', 'ฃ': 'k', 'ค': 'k', 'ฅ': 'k', 'ฆ': 'k',
        'ง': 'ng',
        'จ': 'ch',
        'ฉ': 'ch', 'ช': 'ch',
        'ซ': 's',
        'ฌ': 'ch',
        'ญ': 'y',
        'ฎ': 't',
        'ฏ': 't',
        'ฐ': 't', 'ฑ': 't', 'ฒ': 't',
        'ณ': 'n',
        'ด': 'd',
        'ต': 't',
        'ถ': 't', 'ท': 't', 'ธ': 't',
        'น': 'n',
        'บ': 'b',
        'ป': 'p',
        'ผ': 'ph',
        'ฝ': 'f',
        'พ': 'ph',
        'ฟ': 'f',
        'ภ': 'ph',
        'ม': 'm',
        'ย': 'y',
        'ร': 'r',
        'ฤ': 'rue',
        'ล': 'l',
        'ฦ': 'lue',
        'ว': 'w',
        'ศ': 's',
        'ษ': 's',
        'ส': 's',
        'ห': 'h',
        'ฬ': 'l',
        'อ': 'o',
        'ฮ': 'h',

        '่': '', '้': '', '๊': '', '๋': '', '็': '',
        'ะ': 'a', 'ั': 'a', 'า': 'a',
        'ำ': 'am',
        'ิ': 'i', 'ี': 'i',
        'ึ': 'ue', 'ื': 'ue',
        'ุ': 'u', 'ู': 'u',
        'เ': 'e',
        'แ': 'ae',
        'โ': 'o',
        'ใ': 'ai', 'ไ': 'ai'
	};

	// Make custom replacements
	for (var k in opt.replacements) {
		s = s.replace(RegExp(k, 'g'), opt.replacements[k]);
	}

	// Transliterate characters to ASCII
	if (opt.transliterate) {
		for (var k in char_map) {
			s = s.replace(RegExp(k, 'g'), char_map[k]);
		}
	}

	// Replace non-alphanumeric characters with our delimiter
	var alnum = (typeof(XRegExp) === 'undefined') ? RegExp('[^a-z0-9]+', 'ig') : XRegExp('[^\\p{L}\\p{N}]+', 'ig');
	s = s.replace(alnum, opt.delimiter);

	// Remove duplicate delimiters
	s = s.replace(RegExp('[' + opt.delimiter + ']{2,}', 'g'), opt.delimiter);

	// Truncate slug to max. characters
	s = s.substring(0, opt.limit);

	// Remove delimiter from ends
	s = s.replace(RegExp('(^' + opt.delimiter + '|' + opt.delimiter + '$)', 'g'), '');

	return opt.lowercase ? s.toLowerCase() : s;
}


function convertToSlug(text) {
    return text
        .toLowerCase()
        .replace(/ /g,'-')
        .replace(/[^\w-]+/g,'');
}

function generatePermalink(selector) {
    var permalink = $('input[name=permalink], #id_permalink_readonly');

    if (permalink.val()) {
        return false;
    }

    var before_val = permalink.val();

    selector.keyup(function() {

        if (permalink.hasClass('editing')) {
            return false;
        }

        var text = $(this).val();

        text = convertToSlug(url_slug($(text).text()));

        permalink.val(text).html(text);
    });
}

function controlPermalink() {

    var edit_permalink = $('#edit-permalink');

    $(edit_permalink.attr('href')).hide();

    edit_permalink.click(function (e) {
        e.preventDefault();
        $(this).hide();
        $('#id_permalink_readonly').hide();
        $($(this).attr('href')).addClass('editing').show();

    });
}

function preventScrollReload() {
    $(window).on('beforeunload', function() {
        $(window).scrollTop(0);
    });
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

    if (ilm_length <= 4) {
        $('.load-more-inline').remove();
    }

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


    CKEDITOR.on( 'instanceReady', function( evt ) {

        $('.cke_top').each(function () {

            var calLimit = function () {


                var container = $('.' + $(this).attr('id').replace('_top', ''));
                var limit = container.offset().top + container.outerHeight() - 50;

                return limit;
            }

            var options = {
                marginTop: function () { return $('.navbar-fixed-top').outerHeight(); },
                limit: calLimit,
                removeOffsets: true
            };

            $(this).scrollToFixed(options);
        });

    });



});



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