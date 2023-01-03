
let wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'violet',
    progressColor: 'purple',
    responsive: true
});

let audio = document.getElementById('audioSource').src;
wavesurfer.load(audio);
// wavesurfer.load("http://res.cloudinary.com/dkgm8e6lz/video/upload/v1671732129/cz0pbqmpjg78vm3nxjux.mp3");

//wavesurfer 'ready' event Fires when wavesurfer loads @see events on wave surfer http://wavesurfer-js.org/docs/events.html
wavesurfer.on('ready', function () {
    wavesurfer.setVolume(.7)
    slider = $('#volume-slider')
    slider.val(wavesurfer.getVolume())
    let totalTime = Math.round(wavesurfer.getDuration())
    document.getElementById('time-total').innerText = formatTime(totalTime);
    document.getElementById('time-remaining').innerText = formatTime(totalTime);
    wavesurfer.set
});
if (!wavesurfer.isPlaying()) {
    $('.play-btn').show();
    $('.pause-btn').hide();
} else {
    $('.pause-btn').show();
    $('.play-btn').hide();
}

function playPause() {
    if (wavesurfer.isPlaying()) {
        wavesurfer.pause();
        $('.play-btn').show();
        $('.pause-btn').hide();
    } else {
        wavesurfer.play();
        $('.pause-btn').show();
        $('.play-btn').hide();
    }
}



let panner = wavesurfer.backend.ac.createPanner();

function panAudio(value) {
    let xDeg = parseInt(value);
    let x = Math.sin(xDeg * (Math.PI / 180));
    panner.setPosition(x, 0, 0);

}


let lowpass = wavesurfer.backend.ac.createBiquadFilter();
lowpass.type = 'lowpass'
lowpass.gain.value = 0
lowpass.Q.value = 10
lowpass.frequency.value = 20000

function lowPassFilter(value) {
    lowpass.frequency.value = value
}


let highpass = wavesurfer.backend.ac.createBiquadFilter();
highpass.type = 'highpass'
highpass.gain.value = 0
highpass.Q.value = 10
highpass.frequency.value = 0

function highPassFilter(value) {
    highpass.frequency.value = value
}

function adjustVolume(value){
    let gainSlider = document.getElementById("gain-slider")
        wavesurfer.setVolume(gainSlider.value * value)

}
function adjustGain(value){
    let volumeSlider = document.getElementById("volume-slider");
    wavesurfer.setVolume(volumeSlider.value * value)

}


let analyser = wavesurfer.backend.analyser
frequencyData = new Uint8Array(analyser.frequencyBinCount)
// console.log(analyser)
let formatTime = function (time) {
    return [
        Math.floor((time % 3600) / 60), // minutes
        ('00' + Math.floor(time % 60)).slice(-2) // seconds
    ].join(':');
};




//wavesurfer 'audioprocess' event Fires continuously as the audio plays @see events on wave surfer http://wavesurfer-js.org/docs/events.html
wavesurfer.on('audioprocess', function (e) {

    analyser.getByteFrequencyData(frequencyData);
    // console.log(frequencyData);

    var w = frequencyData[0] * 0.05;
    let audioLevel = document.getElementById('audio-level')
    // console.log(w)
    audioLevel.value = w

    let totalTime = Math.round(wavesurfer.getDuration()),
        currentTime = Math.round(wavesurfer.getCurrentTime()),
        remainingTime = Math.round(totalTime - currentTime);

    document.getElementById('time-current').innerText = formatTime(currentTime);
    document.getElementById('time-remaining').innerText = formatTime(remainingTime);


});

wavesurfer.backend.setFilters([highpass, lowpass, panner]);

