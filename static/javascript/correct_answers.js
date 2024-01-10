$(document).ready(function() {
    $('.correctIcon').click(function() {
        console.log("Correct Answer Handler");
        var answerId = $(this).data('id');
        $.ajax({
            type: 'POST',
            url: '/correct_answer/',
            data: {
                'answer_id': answerId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                if (response.status === 'ok') {
                    var newValue = response.new_value;
                    $(this).parent().find('.AnswerBool').text(newValue);
                }
            }.bind(this)
        });
    });
});