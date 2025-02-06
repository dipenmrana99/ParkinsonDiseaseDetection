function toggleLike() {
    $('#like_button').toggleClass('liked animated');
    // Send AJAX request to update like count in the database
    $.ajax({
        type: 'POST',
        url: '/like',
        data: { action: 'like' },
        success: function(response) {
            if (!response.success) {
                alert('Error: ' + response.error);
            }
        }
    });
    // Reset the animation after 1 second
    setTimeout(function() {
        $('#like_button').removeClass('animated');
    }, 1000);
}

function toggleDislike() {
    $('#dislike_button').toggleClass('disliked animated');
    // Send AJAX request to update dislike count in the database
    $.ajax({
        type: 'POST',
        url: '/dislike',
        data: { action: 'dislike' },
        success: function(response) {
            if (!response.success) {
                alert('Error: ' + response.error);
            }
        }
    });
    // Reset the animation after 1 second
    setTimeout(function() {
        $('#dislike_button').removeClass('animated');
    }, 1000);
}