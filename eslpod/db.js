
function getURLVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function loadScript(url, callback) {
    var script = document.createElement("script")
    script.type = "text/javascript";
    script.onload = function(){
        callback();
    };
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}

function seekAudio(offset) {
    var audio = document.getElementsByTagName("audio")[0];
    audio.currentTime += offset;
    audio.play();
}

function onDocumentReady()
{
    var q = getURLVars()["q"];

    loadScript('./db/'+q+'.js', function () {
        document.getElementById('result').innerHTML = '<pre>'+data+'</pre>';
    });

    text = '';
    text += '<audio controls><source src="./db/'+q+'.mp3" type="audio/mpeg"></audio>\n';
    text += '<br>'
    text += '<button type="button" onclick="seekAudio(-60)">-60</button>\n';
    text += '<button type="button" onclick="seekAudio(-15)">-15</button>\n';
    text += '<button type="button" onclick="seekAudio(+15)">+15</button>\n';
    text += '<button type="button" onclick="seekAudio(+60)">+60</button>\n';

    document.getElementById('audio').innerHTML = text;
}

