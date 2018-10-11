
var highlights = [];
var bMenubox = false;
var xDown = null;
var yDown = null;
var bHLs = false;
var bShowRandom = false;

function saveLocalStorage() {
    localStorage.setItem('highlights', highlights.join('_'));
}

function finalize(element) {
    let word = element.dataset.word;
    let type = element.dataset.type;
    let desc = element.innerHTML;
    let text = '';
    text += '<p>' + word + ' [' + type + ']</p>\n';
    text += '<p>' + desc + '</p>\n';
    element.innerHTML = text;
}

function toggleMenubox(word, posX, posY) {
    let element = document.getElementById('menubox');
    if (!bMenubox && word) {
        element.dataset.selected = word;
        element.style.left = posX + 'px';
        element.style.top = posY + 'px';
        element.style.display = 'block';
        if (posX + element.clientWidth > window.innerWidth)
            element.style.left = (posX - element.clientWidth) + 'px';
        if (posY + element.clientHeight > window.innerHeight)
            element.style.top = (posY - element.clientHeight) + 'px';
        bMenubox = true;
    } else {
        element.style.display = 'none';
        bMenubox = false;
    }
}

function toggleHighlight(word) {
    let element = document.querySelector('div[data-word='+word+']');
    let index = highlights.indexOf(word);
    if (element === null) {
        console.log('invalid element : (word = ' + word + ')');
    }
    else if (index >= 0) {
        element.getElementsByTagName('p')[0].classList.remove('highlight');
        highlights.splice(index, 1);
    }
    else {
        highlights.push(word);
        element.getElementsByTagName('p')[0].classList.add('highlight');
    }
}

function toggleHLs() {
    if (bHLs) {
        bHLs = false;
        showRandom();
    } else {
        bHLs = true;
        showHLs();
    }
}

function onToggleHighlight() {
    let element = document.getElementById('menubox');
    let word = element.dataset.selected;
    if (word && word.length > 0) {
        toggleHighlight(word);
        saveLocalStorage();
    }
}

function onOpenTab(site) {
    let element = document.getElementById('menubox');
    let word = element.dataset.selected;
    if (site == 'webster') {
        window.open('https://www.merriam-webster.com/dictionary/'+word, 'webster');
    } else if (site == 'cambridge') {
        window.open('https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'+word, 'cambridge');
    } else if (site == 'longman') {
        window.open('https://www.ldoceonline.com/dictionary/'+word, 'longman');
    } else if (site == 'dreye') {
        window.open('https://tw.dictionary.yahoo.com/dictionary?p='+word, 'dreye');
    } else if (site == 'database') {
        window.open('db.html?q='+word, 'database');
    }
}

function onClick(event) {
    if (event.target.matches('div[data-word] p')) {
        let element = event.target.parentElement;
        let word = element.dataset.word;
        event.preventDefault();
        toggleMenubox(word, event.clientX, event.clientY);
    } else {
        toggleMenubox(null, 0, 0);
    }
}

function handleTouchStart(event) {
    xDown = event.touches[0].clientX;
    yDown = event.touches[0].clientY;
}

function handleTouchMove(event) {
    if (xDown && yDown) {
        let xUp = event.touches[0].clientX;
        let yUp = event.touches[0].clientY;
        let xDiff = xDown - xUp;
        let yDiff = yDown - yUp;
        if (Math.abs(xDiff) > 10 && Math.abs(yDiff) < 10) {
            if (bShowRandom)
                showRandom();
        }
        xDown = null;
        yDown = null;
    }
}

function onDocumentReady() {

    document.getElementById('result').innerHTML = words;

    let elements = document.querySelectorAll('[data-word]');
    for (let i=0;  i<elements.length; i++) {
        finalize(elements[i]);
    }

    let s_highlights = localStorage.getItem('highlights');
    if (s_highlights !== null) {
        let hls = s_highlights.split('_');
        for (let i=0; i<hls.length; i++) {
            if (hls[i].length > 0)
                toggleHighlight(hls[i]);
        }
    }

    document.addEventListener('click', onClick);
    document.addEventListener('touchstart', handleTouchStart, false);
    document.addEventListener('touchmove', handleTouchMove, false);

    showRandom();
}

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}

function hideAll() {
    let elements = document.querySelectorAll('[data-word]');
    for (let i=0;  i<elements.length; i++)
        elements[i].style.display = 'none';
}

function showAll() {
    let elements = document.querySelectorAll('[data-word]');
    for (let i=0;  i<elements.length; i++)
        elements[i].style.display = 'block';
    bShowRandom = false;
}

function showRandom() {
    hideAll();
    let elements = document.querySelectorAll('[data-word]');
    for (let i=0; i<5; i++)
        elements[getRndInteger(0, elements.length)].style.display = 'block';

    window.scrollTo(0,0);
    let resultEnd = document.getElementById('resultEnd');
    resultEnd.innerHTML = '<p onclick="showHLs()" class="btn">HIGHLIGHT</p>';
    bShowRandom = true;
}

function showHLs() {
    hideAll();
    let elements = document.querySelectorAll('p.highlight');
    for (let i=0;  i<elements.length; i++) {
        elements[i].parentElement.style.display = 'block';
    }

    window.scrollTo(0,0);
    let resultEnd = document.getElementById('resultEnd');
    resultEnd.innerHTML = '';
    resultEnd.innerHTML = '<p onclick="showRandom()" class="btn">RANDOM</p>';
    bShowRandom = false;
}
