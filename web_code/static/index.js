// this is horrifying, can we avoid it?
var dup_flag = true;
var recording = false;
var recorded_once = false;
var audio_context;
var recorder;

function start_user_media(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  // Uncomment if you want the audio to feedback directly
  //input.connect(audio_context.destination);
    config = {
        bufferLen: 4096,
        numChannels: 1,
        mimeType: 'audio/wav'
    };

  recorder = new Recorder(input, config);
}

function start_recording() {
    recorder.record();
    document.getElementById("instructions").innerHTML = "<h3>Click again to stop recording!<\h3>";
}

function stop_recording() {
    recorder.stop();
    
    display_audio();
    recorder.clear();
    
    document.getElementById("instructions").innerHTML = "<h3>Click the button to start recording!<\h3>";
}

function display_audio() {
  recorder && recorder.exportWAV(function(blob) {
    var url = URL.createObjectURL(blob);
    var li = document.createElement('li');
    var au = document.createElement('audio');

    au.controls = true;
    au.src = url;
    li.appendChild(au);
    $('#recordings_list li').length > 0
        ? recordings_list.replaceChild(li, recordings_list.childNodes[0]) 
        : recordings_list.appendChild(li);

    return blob;
  });
}

window.onload = function init() {
  try {
    // webkit shim
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    // navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
    window.URL = window.URL || window.webkitURL;
    
    audio_context = new AudioContext;
  } catch (e) {
    alert('No web audio support in this browser!');
  }
  
  navigator.mediaDevices.getUserMedia({audio: true}).then(start_user_media);

  document.getElementById("record_button").addEventListener("click", function() {
        if (dup_flag) {
            if(recorded_once) {
                css_rule = get_CSS_rule('.recordings_paragraph');
                css_rule.style.display = 'initial';
            }
            else
                recorded_once = true;

            if(recorder && !recording) {
                start_recording();
            }
            
            if (recording) stop_recording();
            recording = !recording;
        }
        dup_flag = !dup_flag;
    });
};

// helpful utility
function get_CSS_rule(ruleName, deleteFlag) {               // Return requested style obejct
   ruleName=ruleName.toLowerCase();                       // Convert test string to lower case.
   if (document.styleSheets) {                            // If browser can play with stylesheets
      for (var i=0; i<document.styleSheets.length; i++) { // For each stylesheet
         var styleSheet=document.styleSheets[i];          // Get the current Stylesheet
         var ii=0;                                        // Initialize subCounter.
         var cssRule=false;                               // Initialize cssRule. 
         do {                                             // For each rule in stylesheet
            if (styleSheet.cssRules) {                    // Browser uses cssRules?
               cssRule = styleSheet.cssRules[ii];         // Yes --Mozilla Style
            } else {                                      // Browser usses rules?
               cssRule = styleSheet.rules[ii];            // Yes IE style. 
            }                                             // End IE check.
            if (cssRule)  {                               // If we found a rule...
               if (cssRule.selectorText.toLowerCase()==ruleName) { //  match ruleName?
                  if (deleteFlag=='delete') {             // Yes.  Are we deleteing?
                     if (styleSheet.cssRules) {           // Yes, deleting...
                        styleSheet.deleteRule(ii);        // Delete rule, Moz Style
                     } else {                             // Still deleting.
                        styleSheet.removeRule(ii);        // Delete rule IE style.
                     }                                    // End IE check.
                     return true;                         // return true, class deleted.
                  } else {                                // found and not deleting.
                     return cssRule;                      // return the style object.
                  }                                       // End delete Check
               }                                          // End found rule name
            }                                             // end found cssRule
            ii++;                                         // Increment sub-counter
         } while (cssRule)                                // end While loop
      }                                                   // end For loop
   }                                                      // end styleSheet ability check
   return false;                                          // we found NOTHING!
}                                                         // end get_CSS_rule 