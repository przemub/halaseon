function ajax( options ) {
options = {
    type: options.type || "POST",
    url: options.url || "",
    onComplete: options.onComplete || function(){},
    onError: options.onError || function(){},
    onSuccess: options.onSuccess || function(){},
    dataType: options.dataType || "text"
};

var xml = new XMLHttpRequest();
xml.open(options.type, options.url, true);

xml.onreadystatechange = function(){
    if ( xml.readyState == 4) {
        if ( httpSuccess( xml ) ) {
            var returnData = (options.dataType=="xml")? xml.responseXML : xml.responseText
            options.onSuccess( returnData );
        } else {
            options.onError();
        }
        options.onComplete();
        xml = null;
    }
};

xml.send();

function httpSuccess(r) {
        try {
            return ( r.status >= 200 && r.status < 300 || r.status == 304 || navigator.userAgent.indexOf("Safari") >= 0 && typeof r.status == "undefined")
        } catch(e) {
            return false;
        }
    }
}
