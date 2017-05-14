document.addEventListener("DOMContentLoaded", init, false);

window.AudioContext = window.AudioContext || window.webkitAudioContext;
var context = new window.AudioContext();
var Recorder = require('./lib/recorder');
var recorder;
var qid;

function init () {
    var questions = requestQuestions();
    var audioPlay = document.getElementById("question");
    audioPlay.onclick = audioClick;

    var recordBtn = document.getElementById("mic");
    recordBtn.onclick = micClick;

    navigator.mediaDevices.getUserMedia({audio: true}).then(startUserMedia).catch(
        function(e) {
              console.log('No live audio input: ' + e);
        }
    );
}


var concatBuffs = function(buff1, buff2) {
    var numChannels = Math.min( buff1.numberOfChannels, buff2.numberOfChannels );
    var temp = context.createBuffer( numChannels, (buff1.length + buff2.length), buff1.samplerate);

    for (var i=0; i < numChannels; i++) {
        var channel = temp.getChannelData(i);
        channel.set( buff1.getChannelData(i), 0);
        channel.set( buff2.getChannelData(i), buff1.length);
    }
    return temp;
};


var requestQuestions = function() {
    var url = 'https://pdcmadlib.radiocut.fm/backend/list_madlibs';
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                parseQuestions(request.responseText);
            } else {
                console.log('err: ' + request.status);
            }
        }
    };
    request.open('GET', url, true);
    request.send();
}

var parseQuestions = function(questions) {
    var parsed = JSON.parse(questions);
    var ind = Math.floor(Math.random() * parsed.length);
    injectQuestion(parsed[ind]);
}

var injectQuestion = function(question) {
    var base_url = 'https://pdcmadlib.radiocut.fm/media/';
    var text = question.question;
    var interviewer = question.interviewer;
    qid = question.key;
    var clip = question.parts[0];
    var link = question.link;

    var div_interviewer = document.getElementById("question-interviewer");
    var div_question = document.getElementById("question-question");
    var div_source = document.getElementById("question-source");
    var audio = document.getElementById("question-audio");

    var node = document.createElement("a");
    node.href = link;
    node.innerHTML = 'Full interview';
    div_source.appendChild(node);

    div_interviewer.innerHTML = interviewer;
    div_question.innerHTML = text;
    audio.setAttribute("src", base_url + clip.file);
}

var playing = false;
var audioClick = function() {
    var audio = document.getElementById("question-audio");
    var wrapper = document.getElementById("question");

    if (!playing) {
        audio.addEventListener("ended", onEnd, false);
        audio.play();
        wrapper.style.background = "grey";
        playing = true;
    } else {
        audio.pause();
        wrapper.style.background = "none";
        playing = false;
    }
}

var onEnd = function() {
    var wrapper = document.getElementById("question");
    wrapper.style.background = "none";
    playing = false;
}

var recording = false;
var micClick = function() {
    var recordImg = document.getElementById("mic").childNodes[1];
    if (!recording) {
        recordImg.setAttribute("src", "images/redMic.svg");
        recorder && recorder.record();
        recording = true;
    } else {
        recorder && recorder.stop();
        recordImg.setAttribute("src", "images/mic.svg");
        recorder && recorder.exportWAV(writeAudioToDisk);
        //recorder.getBuffer(getBufferCallback);
        recording = false;
    }
}

var getBufferCallback = function( buffers ) {
    var newSource = context.createBufferSource();
    var newBuff = context.createBuffer( 2, buffers[0].length, context.sampleRate );
    newBuff.getChannelData(0).set(buffers[0]);
    newBuff.getChannelData(1).set(buffers[1]);
    newSource.buffer = newBuff;
    writeAudioToDisk(newSource);
}

var writeAudioToDisk = function (blob) {
    var request = new XMLHttpRequest();
    var url = 'https://pdcmadlib.radiocut.fm/backend/send_recording/' + qid + '/';
    //var url = 'https://pdcmadlib.localtunnel.me';
    console.log('audio recorded!', blob);
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                console.log('200 sent! ' + request);
                var share = document.getElementById("share");
                share.style.display = "block";
                var response = JSON.parse(request.response);
                var shareBtn = document.getElementById("share-button");
                shareBtn.href = response.url;
            } else {
                console.log('err: ' + request.status);
            }
        }
    };
    var formData = new FormData();
    request.open('POST', url, true);
    formData.append("data", blob);
    request.send(formData);
}

function startUserMedia(stream) {
    console.log('Running user media');
    var input = context.createMediaStreamSource(stream);
    recorder = new Recorder(input);
}
