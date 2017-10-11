
function renderEntry() {
    $('.entry').each( function() {
        var link = $(this).attr('link');
        var title = $(this).attr('title');
        var image = $(this).attr('image');
        var text = '';
        text += '<a href="'+link+'">';
        text += '<h2>'+title+'</h2>';
        if (image)
            text += '<img src="'+image+'" class="img" />';
        text += '</a>';
        $(this).html(text);
    });
}

function renderVideo() {
    $('.video').each( function() {
        var src = $(this).attr('src');
        var type = $(this).attr('type');
        var text = '';
        text += '<video controls>';
        text += '<source src="'+src+'" type="'+type+'">';
        text += '</video>';

        $(this).html(text);
    });
}

function renderAudio() {
    $('.audio').each( function() {
        var src = $(this).attr('src');
        var type = $(this).attr('type');
        var text = '';
        text += '<audio controls preload=none style="width:800px;">';
        text += '<source src="'+src+'" type="'+type+'">';
        text += '</audio>';
        $(this).html(text);
    });
}

function renderWord() {
    var text = '';
    var words = $('.word').toArray();
    for (var i in words) {
        var target = $(words[i]).attr('target');
        var href = $(words[i]).attr('href');
        var word = $(words[i]).attr('word');
        text += '<li class="word"><a target="'+target+'" href="'+href+'">'+word+'</a></li>';
    }
    $('#result_words').html(text);
}

function onKeyDown(e) {
    if ($('audio').length > 0) {
        switch (e.which) {
            case 37: // left
                $('audio').prop("currentTime",$("audio").prop("currentTime")-5);
                e.preventDefault(); // prevent the default action
                break;
            case 39: // right
                $('audio').prop("currentTime",$("audio").prop("currentTime")+5);
                e.preventDefault(); // prevent the default action
                break;
            case 32: // space
                if ($('audio').get(0).paused == false)
                    $('audio').trigger('pause');
                else
                    $('audio').trigger('play');
                e.preventDefault(); // prevent the default action
                break;
            default:
                break;
        }
    }
}

function onReady() {
    renderEntry();
    renderVideo();
    renderAudio();
    renderWord();
    $(document).keydown(onKeyDown);
}
