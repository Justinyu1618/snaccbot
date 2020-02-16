$(document).ready(function() {
    $('.send').click(function() {
        const request_id = $(this).attr('data-id');
        $.post('/send', {
            'request_id': request_id
        }).fail( function(xhr, textStatus, errorThrown) {
            alert(xhr.responseText);
        }).always(function() {
            location.reload();
        });
    });

    $('#mark-home').click(function() {
        $.post('/mark_home').always(function() {
            location.reload();
        });
    });

    $('.mark-complete').click(function() {
        const request_id = $(this).attr('data-id');
        $.post('/mark_complete', {
            'request_id': request_id
        }).always(function() {
            location.reload();
        })
    });
});
