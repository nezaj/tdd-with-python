jQuery(document).ready(function () {
    $('body').on('keypress', '#id_text', function () {
        $('.has-error').hide();
    });

    $('body').on('click', '#id_text', function () {
        $('.has-error').hide();
    });
});
