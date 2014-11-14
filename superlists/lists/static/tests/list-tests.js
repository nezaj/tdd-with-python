test("errors should be hidden on keypress", function () {
    $("#id_text").trigger('keypress');
    equal($('.has-error').is(':visible'), false);
});

test("errors should be hidden on click", function () {
    $("#id_text").trigger('click');
    equal($('.has-error').is(':visible'), false);
});

test("errors not hidden unless there is a keypress", function () {
    equal($('.has-error').is(':visible'), true);
});
