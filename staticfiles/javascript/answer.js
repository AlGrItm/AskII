$(".answerIcon").on('click', function (ev) {
    console.log("Like Answer Handler");
    const answerId = $(this).data('id');
    const csrftoken = getCookie('csrftoken');
    fetch('/like_answer/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'answer_id=' + answerId,
    }).then(response =>
        response.json().then(data => {
            $(this).siblings(".LikeCount").text(data.likes_count);
        })
    );
});