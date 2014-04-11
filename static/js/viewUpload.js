/* global $, console, analytics */

/* Button Click Event */

$('.upload').click(function() {
    var $this = $(this);
    $('#session-link').hide();
    if (!$this.hasClass('active')) {
        $('.upload').removeClass('active');
        $(this).addClass('active');
        $('form').toggle();
    }
});

/* Error Function */
function showError() {
    $('#progress').toggle();
    $('#session-link').attr('href', '.').removeAttr('target').text('Something went wrong while converting...').show();
}

/* Form Submit Events */

function fetchSession(documentID, expire) {
    var data = new FormData();
    data.append('document_id', documentID);
    data.append('expire', expire);

    $.ajax({
        type: 'POST',
        contentType: false,
        processData: false,
        data: data,
        dataType: 'json',
        url: 'sessions',
        error: function (data) {
            console.log(data);
            showError();
        },
        statusCode: {
            200: function(data) {
                $('button, #progress').toggle();
                $('#session-link').text(data.session_url).attr('href', data.session_url).show();
                $('html, body').delay(1000).animate( {scrollTop: $('#session-link').offset().top}, 2000);
                $('iframe').attr('src', data.session_url).delay(1000).fadeIn('slow');
            },
            202: function() {
                fetchSession(documentID, expire);
            }
        }
    });
}

$('#desktop-upload-form').submit(function () {
    $('button').blur();

    var data = new FormData();
    data.append('file', $('#file')[0].files[0]);
    var shouldExpire = $('#desktop-expiration').is(':checked') ? 'no_expire' : 'expire';

    $('button, #progress').toggle('fast');
    $.ajax({
        type: 'POST',
        contentType: false,
        processData: false,
        data: data,
        dataType: 'json',
        url: 'desktop-upload',
        error: function (data) {
            console.log(data);
            showError();
            analytics.track('Desktop Conversion', {
                success: 'false'
            });
        }
    }).done(function (data) {
        console.log('Document ID is: ' + data.id);
        fetchSession(data.id, shouldExpire);
        analytics.track('Desktop Conversion', {
            success: 'true'
        });
    });

    return false;
});

$('#url-upload-form').submit(function () {
    $('button').blur();

    var data = new FormData();
    data.append('document-url', $('#file-url').val());
    var shouldExpire = $('#url-expiration').is(':checked') ? 'no_expire' : 'expire';

    $('button, #progress').toggle('fast');
    $.ajax({
        type: 'POST',
        contentType: false,
        processData: false,
        data: data,
        dataType: 'json',
        url: 'url-upload',
        error: function (data) {
            console.log(data);
            showError();
            analytics.track('URL Conversion', {
                success: 'false'
            });
        }
    }).done(function (data) {
        console.log('Document ID is: ' + data.id);
        fetchSession(data.id, shouldExpire);
        analytics.track('URL Conversion', {
            success: 'true'
        });
    });

    return false;
});
