document.addEventListener("DOMContentLoaded", init, false);

function init () {
    var questions = requestQuestions();
}

var context = new window.AudioContext();
var Recorder = require('./lib/recorder');

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

var captureMic = function(source) {
    var rec = new Recorder(source);
    // rec.record();
    // rec.stop();
    // var newClip = rec.getBuffer([callback]);
}

var getBufferCallback = function( buffers ) {
    var newSource = context.createBufferSource();
    var newBuff = context.createBuffer( 2, buffers[0].length, context.sampleRate );
    newBuff.getChannelData(0).set(buffers[0]);
    newBuff.getChannelData(1).set(buffers[1]);
    newSource.buffer = newBuff;

    return newBuff;
}

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
    var text = question.question;
    var interviewer = question.interviewer;
    var id = question.key;
    var clip = question.parts[0];
    console.log('Interviewer: ', interviewer);
    console.log('question: ', text);
    console.log('key: ', id);
}
