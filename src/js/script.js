document.addEventListener("DOMContentLoaded", init, false);

var context = new window.AudioContext();
var Recorder = require('./lib/recorder');
var recorder;
var qid;

function init () {
    var questions = requestQuestions();
    var audioPlay = document.getElementById("question-icon");
    audioPlay.onclick = audioClick;

    var recordBtn = document.getElementById("mic");
    recordBtn.onclick = micClick;

    navigator.getUserMedia(
        {audio: true},
        startUserMedia,
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
    var url = 'http://pdcmadlib.radiocut.fm/backend/list_madlibs';
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
    var base_url = 'http://pdcmadlib.radiocut.fm/media/';
    var text = question.question;
    var interviewer = question.interviewer;
    qid = question.key;
    var clip = question.parts[0];

    var div_interviewer = document.getElementById("question-interviewer");
    var div_question = document.getElementById("question-question");
    var audio = document.getElementById("question-audio");

    div_interviewer.innerHTML = interviewer;
    div_question.innerHTML = text;
    audio.setAttribute("src", base_url + clip.file);
}

var playing = false;
var audioClick = function() {
    var audio = document.getElementById("question-audio");

    if (!playing) {
        audio.play();
        playing = true;
    } else {
        audio.pause();
        playing = false;
    }
}

var recording = false;
var micClick = function() {
    if (!recording) {
        recorder.record();
        recording = true;
    } else {
        recorder.stop();
        recorder.exportWAV(writeAudioToDisk);
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
    var url = 'http://pdcmadlib.radiocut.fm/backend/send_recording/' + qid + '/';
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                // lets hope the server catches it!
                console.log('sent! ' + request);
            } else {
                console.log('err: ' + request.status);
            }
        }
    };
    request.open('POST', url, true);
    request.send(blob);
}

function startUserMedia(stream) {
    var input = context.createMediaStreamSource(stream);
    recorder = new Recorder(input);
}
