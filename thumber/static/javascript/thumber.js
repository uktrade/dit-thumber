var thumber = (function ($) {

    var form = $('.thumber-form'),
        radio_input = $('.thumber-form input[type=radio]'),
        radio_label = $('label[for=' + $(radio_input[0]).attr('id') + '], label[for=' + $(radio_input[1]).attr('id') + ']'),
        textarea_input = $('.thumber-form textarea'),
        textarea_label = $('label[for=' + textarea_input.attr('id') + ']'),
        submit = $('.thumber-form input[type=submit]'),
        thanks_holder = $('.thumber-success'),
        error_holder = $('.thumber-error'),
        success = null,
        error = null,
        radio, textarea, id;

    radio = radio_input.add(radio_label);
    textarea = textarea_input.add(textarea_label);

    thanks_holder.hide();
    error_holder.hide();
    textarea.hide();
    submit.hide();

    radio_input.on('change', handleForm);
    form.on('submit', handleForm);

    function handleForm(event) {

        var data = {
            'thumber_token': 'ajax',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]', form).val()
        };

        switch($(event.currentTarget).val()) {
            case 'False':
                data.satisfied = 'False';
                $.when(feedbackRequest(data))
                    .done(function (response) {
                        id = response.id;
                        radio.hide()
                        textarea.show();
                        submit.show();
                    })
                    .fail(function () {
                        handleError();
                    });
                break;
            case 'True':
                data.satisfied = 'True';
                $.when(feedbackRequest(data))
                    .done(function () {
                        form.hide();
                        handleSuccess();
                    })
                    .fail(function () {
                        handleError();
                    });
                break;
            default:
                event.preventDefault();
                data.id = id;
                data.comment = textarea_input.val();

                $.when(feedbackRequest(data))
                    .done(function () {
                        form.hide();
                        handleSuccess();
                    })
                    .fail(function () {
                        handleError();
                    });
        }
    }

    function handleSuccess() {
        if (success !== null) {
            success();
        } else {
            thanks_holder.show();
        }
    }

    function handleError() {
        if (error !== null) {
            error();
        } else {
            form.hide();
            error_holder.show();
        }
    }

    function setSuccessHandler(func) {
        success = func
    }

    function setErrorHandler(func) {
        error = func
    }

    function feedbackRequest(data) {

        var feedback = $.ajax({
            url: form.attr('action'),
            type: 'POST',
            dataType: 'json',
            data: data
        });

        return feedback;
    }

    return {
        setSuccessHandler: setSuccessHandler,
        setErrorHandler: setErrorHandler,
    }

}(jQuery));
