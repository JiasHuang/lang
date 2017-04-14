
function renderEntry() {
    $('.div_entry').each( function() {
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
    $('.div_video').each( function() {
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
    $('.div_audio').each( function() {
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
    $('.div_word').each( function() {
        var target = $(this).attr('target');
        var href = $(this).attr('href');
        var word = $(this).attr('word');
        text = '<li class="word">'+word+'<a target="'+target+'" href="'+href+'">['+target+']</a></li>';
        $(this).html(text);
    });
}

function onReady() {
    renderEntry();
    renderVideo();
    renderAudio();
    renderWord();
}
