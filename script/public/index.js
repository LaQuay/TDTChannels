// Se espera en la URL este tipo de llamada .html?type={audio,video}&channel={url_a_reproducir}
function loadItem(from) {
    var value;
    if (from == "audio") {
        value = document.getElementById("input-reproduccion-audio").value;
        reproduceAudio(value);
    } else if (from == "video") {
        value = document.getElementById("input-reproduccion-video").value;
        reproduceVideo(value);
    }
}

function reproduceVideo(channelToReproduce) {
    console.log("Reproducing video: " + channelToReproduce);
    if (channelToReproduce.includes("m3u8")) {
        var divInfo = document.getElementById("video-player").childElementCount;
        if (divInfo == 0) {
            player = new Clappr.Player({
                source: channelToReproduce,
                parentId: '#video-player',
                height: '500px',
                width: '100%',
                autoPlay: true,
            });
        } else {
            // Assume player instance is already created
            player.configure({
              source: channelToReproduce,
            });
        }
        clearResolutions();
        getResolution(channelToReproduce, updateResolution);
    }

    ga('send', {
      hitType: 'event',
      eventCategory: 'Video',
      eventAction: 'play',
      eventLabel: channelToReproduce
    });
}

function reproduceAudio(channelToReproduce) {
    if (channelToReproduce.includes("pls")) {
        getURLsFromPLS(channelToReproduce, reproducePLSFromUrl);
    } else {
        reproduceAudioFromUrl(channelToReproduce);
    }
}

function reproduceAudioFromUrl(channelToReproduce) {
    console.log("Reproducing audio: " + channelToReproduce);
    var audioSource = document.getElementById('audio-controller');
    var audioPlayer = document.getElementById('audio-player');

    audioPlayer.src = channelToReproduce;
    audioSource.load();
    audioSource.pause();

    var playPromise = audioSource.play();
    if (playPromise !== undefined) {
      playPromise.then(function() {
        // Automatic playback started!
      }).catch(function(error) {
        // Automatic playback failed.
        // Show a UI element to let the user manually start playback.
      });
    }

    ga('send', {
      hitType: 'event',
      eventCategory: 'Audio',
      eventAction: 'play',
      eventLabel: channelToReproduce
    });
}

function reproducePLSFromUrl(data) {
    reproduceAudioFromUrl(data[0]);
    updateExtraAudioInfo("pls_more_url_available", data);
}

function updateResolution(resolutions) {
    console.log("Resoluciones: " + resolutions);

    for (i = 0; i < resolutions.length; i++) {
        var resolutionToAdd = resolutions[i];
        if (i < resolutions.length - 1){
            resolutionToAdd += ", ";
        }
        document.getElementById("video-resolution").innerHTML += resolutionToAdd;
    }
}

function clearResolutions() {
    document.getElementById("video-resolution").innerHTML = "";
}

function updateExtraAudioInfo(type, data) {
    console.log("Extra info type: " + type);
    console.log("Extra info data: " + data);

    var textToAdd = "";
    if (type == "pls_more_url_available") {
        for (i = 0; i < data.length; i++) {
            textToAdd += data[i] + "<br>";
        }
    }

    document.getElementById("extra-audio-info").innerHTML = textToAdd;
    document.getElementById("extra-audio-info-div").style.display = "block";
}

function getURLsFromPLS(sUrl, fn_callback) {
    $.get(sUrl, function(data) {
        $response = data.split("\n");

        $urls=[];
        $.each($response, function( index, value ) {
            $line_separated_value = value.split("=");
            if ($line_separated_value.length > 1 && $line_separated_value[1].indexOf("http") != -1) {
                $urls.push($line_separated_value[1]);
            }
        });
        fn_callback($urls)
    });
};

function getResolution(from, fn_callback) {
    $.get(from, function(data) {
        $response = data.split("\n");

        $resolutions=[];
        $.each($response, function( index, value ) {
            $line_separated_value = value.split(",");
            for (i = 0; i < $line_separated_value.length; i++) {
                if ($line_separated_value[i].indexOf("RESOLUTION=") != -1) {
                    $resolutions.push($line_separated_value[i].split('=')[1]);
                }
            }
        });

        fn_callback($resolutions);
    });
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function filterChannelsList() {
    var input, filter, div, elements, txtValue;

    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("channel-list");
    elements = div.getElementsByTagName("a");

    for (i = 0; i < elements.length; i++) {
        txtValue = elements[i].textContent || elements[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            elements[i].style.display = "";
        } else {
            elements[i].style.display = "none";
        }
    }
}

function reproduceChannel(channel_options) {
    document.getElementById("option-buttons").innerHTML = ""
    if (channel_options.length > 0) {
        reproduceVideo(channel_options[0]['url'])

        if (channel_options.length > 1) {
            for (i = 0; i < channel_options.length; ++i) {
                var url = channel_options[i]['url'];
                document.getElementById("option-buttons").innerHTML +=
                    "<a href='javascript:reproduceVideo(\"" + url + "\")' class='btn btn-secondary btn-sm' style='margin-right: 10px'>Opción " + (i+1) + "</a>";
            }
        }
    } else {
        reproduceVideo("no_video_found.m3u8")
    }
}

function onChannelClick(channel) {
    channel = JSON.parse(channel);
    reproduceChannel(channel['options'])

    if (document.getElementById("container").offsetWidth < 720) {
        document.getElementById("video").scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
    }
}

function loadChannelsInList() {
    fetch('http://91.121.64.179/tdt_project/output/channels.json')
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        nacionales = myJson["countries"][0]; //Spain is the [0] country

        var items = [];
        $.each(nacionales["ambits"], function( ambit, ambit_val ) {
            $.each(ambit_val["channels"], function( key, val ) {
                items.push("<a href='javascript:onChannelClick(" + JSON.stringify(JSON.stringify(val)) + ")' class='list-group-item list-group-item-action'>" + val["name"] + "</a>")
            });
        });

        $(items.join( "" )).appendTo(".channels-list");
      });
}