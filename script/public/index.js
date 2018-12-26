function getURLsFromPLS(sUrl, fn_callback) {
    var from = "http://provisioning.streamtheworld.com/pls/CADENADIAL.pls";
    $.get(from, function(data) {
        $response = data.split("\n");

        $urls=[];
        $.each($response, function( index, value ) {
            $line_separated_value = value.split("=");
            if ($line_separated_value.length > 1 && $line_separated_value[1].indexOf("http") != -1) {
                $urls.push($line_separated_value[1]);
            }
        });
        fn_callback($urls)

        //$.each($urls, function( index, value ) {
        //    if (checkIfWebsiteWorks(value)) {
        //        fn_callback(value);
        //        break;
        //    }
        //});
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

// Check an URL is valid or broken
// TODO: For streams if it works it keeps loading infinite time
function checkIfWebsiteWorks(sUrl){
    $.get(sUrl, function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
    });
}