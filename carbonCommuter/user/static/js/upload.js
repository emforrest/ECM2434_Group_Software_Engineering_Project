
function onLoad(tab = "") {
    window.attempts = 0;
    window.last_accuracy = "0";
    
    if (tab != "") {
        window.current_tab = parseInt(tab);
    } else {
        window.current_tab = 1;
    }

    if (window.current_tab > 0) {
        window.current_tab = 0;
        nextTab();
        getLocation();
    }
}

function showManualInput() {
    document.getElementById("manual_select").style.display = "block";
    document.getElementById("btn_input").style.display = "none";
    document.getElementById("btn_continue").style.width = "100%"
}

function hideManualInput() {
    document.getElementById("manual_select").style.display = "none";
    document.getElementById("btn_input").style.display = "inline-block";
    document.getElementById("btn_continue").style.width = "49%"
}

function nextTab() {
    document.getElementById(`tab${window.current_tab}`).style.display = "none";
    window.current_tab++;
    document.getElementById(`tab${window.current_tab}`).style.display = "block";
    hideError();
}

function prevTab() {
    document.getElementById(`tab${window.current_tab}`).style.display = "none";
    window.current_tab--;
    document.getElementById(`tab${window.current_tab}`).style.display = "block";
    hideError();
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(checkAccuracy, handleError, {enableHighAccuracy: true, maximumAge: 1000});
    } else { 
        alert("Geolocation is not supported by this browser.");
    }
}

function checkAccuracy(position) {
    if (window.current_tab > 1) {
        showPosition(position);
    } else if (parseFloat(position.coords.accuracy) < 300) {
        showPosition(position);
        setTimeout(nextTab, 2000);
    } else {
        window.attempts++;
        if (window.attempts >= 3 && Math.abs(parseFloat(window.last_accuracy) - parseFloat(position.coords.accuracy)) <= 0.001) {
            showPosition(position);
            accuracyErrorOnLoad();
            setTimeout(nextTab, 3000);
        } else if (window.attempts < 5) {
            window.last_accuracy = position.coords.accuracy;
            setTimeout(getLocation, 5000);
        } else {
            showPosition(position);
            accuracyErrorOnLoad();
            setTimeout(nextTab, 3000);
        }
    }
}

function accuracyErrorOnLoad() {
    console.log("Couldn't get an accurate location!");
    window.error = "Failed to get an accurate location! You may need to adjust it manually...";
    document.getElementById("loading").style.display = "none";
    showError();
}

function showPosition(position) {
    setLatLong(position.coords.latitude, position.coords.longitude);
    getAddress(position);
}

function showError() {
    document.getElementById("error").innerHTML = window.error;
    document.getElementById("error").style.display = "block";
}

function hideError() {
    document.getElementById("error").style.display = "none";
}

function handleError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.")
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.")
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.")
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.")
            break;
    }
}

function getAddress(position) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `https://maps.googleapis.com/maps/api/geocode/json?latlng=${position.coords.latitude},${position.coords.longitude}&key=AIzaSyCVEKGGBT_8WryClHT64tPqFONldHdY35Y`);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            const results = xhr.response;
            setAddress(results['results'][0]['formatted_address']);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
}

let autocomplete;
function initAutocomplete(){
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        {
        types:['address'],
        componentRestrictions: {'country': ['gb']},
        fields : ['geometry', 'formatted_address'],
        strictBounds: true
        }
    );
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged(){
    var place = autocomplete.getPlace();
    if (place.geometry) {
        console.log(place.formatted_address);
        setAddress(place.formatted_address);
        setLatLong(place.geometry.location.lat().toString(), place.geometry.location.lng().toString());
        hideManualInput();
    }
}

function setAddress(address) {
    document.getElementById('address').value = address;
    document.getElementById('display_address').innerHTML = address;
}

function setLatLong(lat, long) {
    document.getElementById('lat').value = lat;
    document.getElementById('long').value = long;
    document.getElementById('google_map').setAttribute('src', `https://maps.google.co.uk?q=${lat},${long}&output=embed`);
}