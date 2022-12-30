// let audio = {
//     init: function () {
//         let $that = this;
//         $(function () {
//             $that.components.media();
//         });
//     },
//     components: {
//         media: function (target) {
//             let media = $('audio.fc-media', (target !== undefined) ? target : 'body');
//             if (media.length) {
//                 media.mediaelementplayer({
//                     audioHeight: 40,
//                     features: ['playpause', 'current', 'duration', 'progress', 'volume', 'tracks', 'fullscreen'],
//                     alwaysShowControls: true,
//                     timeAndDurationSeparator: '<span></span>',
//                     // iPadUseNativeControls: true,
//                     // iPhoneUseNativeControls: true,
//                     // AndroidUseNativeControls: true
//                 });
//             }
//         },
//
//     },
// };
//
// audio.init();
let wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'violet',
    progressColor: 'purple',

});
let source = document.getElementById('audioSource').src;
wavesurfer.load(source);
console.log(wavesurfer, wavesurfer.isPlaying())
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


wavesurfer.on('ready', function () {
    wavesurfer.setVolume(.7)
    slider = $('#volume-slider')
    console.log(slider.val())
    slider.val(wavesurfer.getVolume() * 100)
    console.log(wavesurfer.getVolume() * 100)
});

let panner = wavesurfer.backend.ac.createPanner();
wavesurfer.backend.setFilter(panner);

// let slider = document.querySelector('#panner-input');
// slider.addEventListener('input', function (e) {
//     var xDeg = parseInt(e.target.value);
//     var x = Math.sin(xDeg * (Math.PI / 180));
//     wavesurfer.panner.setPosition(x, 0, 0);
// });
function panAudio(value){
    var xDeg = parseInt(value);
    var x = Math.sin(xDeg * (Math.PI / 180));
   panner.setPosition(x, 0, 0);

}

