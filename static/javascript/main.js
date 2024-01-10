function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".questionIcon").on('click', function (ev) {
    const questionId = $(this).data('id');
    const csrftoken = getCookie('csrftoken');

    fetch('/like/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'question_id=' + questionId,
    }).then(response =>
        response.json().then(data => {
            $(this).siblings(".LikeCount").text(data.likes_count);
        })
    );
});
