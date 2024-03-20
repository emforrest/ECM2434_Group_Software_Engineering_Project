
function onLoad(tab = 1) {
    window.attempts = 0;
    window.last_accuracy = "0";

    var form = document.getElementById("journey_form");
    form.addEventListener("submit", onSubmit, true);

    window.current_tab = tab;
    document.getElementById(`tab${tab}`).style.display = "block";

    if (window.error != "") {
        showError();
    }
    if (window.current_tab == 1) {
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
        window.error = "Geolocation is not supported by this browser. Please switch browser to keep using the service!"
        showError();
        showLocationOff();
    }
}

function checkAccuracy(position) {
    if (window.current_tab == 2) {
        showPosition(position);
    } else if (parseFloat(position.coords.accuracy) <= 300) {
        showPosition(position);
        setTimeout(nextTab, 3000);
    } else {
        window.attempts++;
        if ((window.attempts >= 2 && Math.abs(parseFloat(window.last_accuracy) - parseFloat(position.coords.accuracy)) <= 0.001) || (window.attempts > 3)) {
            accuracyErrorOnLoad();
            setTimeout(nextTab, 2000);
        } else {
            window.last_accuracy = position.coords.accuracy;
            setTimeout(getLocation, 3000);
        }
    }
}

function accuracyErrorOnLoad() {
    console.log("Couldn't get an accurate location!");
    window.error = "Failed to get an accurate location! Please enter it manually...";
    document.getElementById("loading").style.display = "none";
    showError();
}

function showPosition(position) {
    setLatLong(position.coords.latitude, position.coords.longitude);
    document.getElementById("btn_refresh").innerHTML = "Re-fetch Location"
    getAddress(position);
}

function showError() {
    document.getElementById("error_msg").innerHTML = window.error;
    document.getElementById("error").style.display = "block";
}

function hideError() {
    document.getElementById("error").style.display = "none";
}

function showLocationOff() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("animation").style.display = "none";
    document.getElementById("location").style.display = "block";
    document.getElementById("btn_failed").style.display = "block";
}

function handleError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            window.error = "It seems you have your location turned off. CarbonCommuter requires location data for verifying journeys! Please allow location services and try again!";
            break;
        case error.POSITION_UNAVAILABLE:
            window.error = "We're sorry, it seems location information is unavailable right now. Please try again later!";
            break;
        case error.TIMEOUT:
            window.error = "The request to get user location timed out. Please try again!";
            break;
        case error.UNKNOWN_ERROR:
            window.error = "We're sorry, an unknown error occurred whilst fetching your location. Please try again.";
            break;
    };
    showError();
    showLocationOff();
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

function verifyAddress() {
    if (document.getElementById("lat").value == "") {
        window.error = "You must fetch your location before continuing!";
        showError();
        return false;
    } else if (document.getElementById("long").value == "") {
        window.error = "You must fetch your location before continuing!";
        showError();
        return false;
    } else if (document.getElementById("address").value == "") {
        window.error = "You must fetch your location before continuing!";
        showError();
        return false;
    } else {
        return true;
    }
}

function onSubmit(event) {
    var valid = true;
    if (document.getElementById("transport") != null) {
        if (document.getElementById("transport").value == "") {
            valid = false;
            window.error = "You must select a method of transport!";
            showError();
        }
    }

    if (!verifyAddress()) {
        if (window.current_tab == 3) {
            prevTab();
        }
        valid = false;
    }

    if (!valid) {
        console.log("preventing default");
        event.preventDefault();
    }
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

function showInfo(option) {
    document.getElementById("additional-info").style.display = "block";
    var infoContainer = document.getElementById("additional-info");
    if (option === 'Bus') {
        infoContainer.innerHTML = "<p>Compared to an average car you are saving:<br>33% of CO2</p>";
    } else if (option === 'Train') {
        infoContainer.innerHTML = "<p>Compared to an average car you are saving:<br>72.6% of CO2</p>";
    } else if (option === 'Bike') {
        infoContainer.innerHTML = "<p>Compared to an average car you are saving:<br>86% of CO2</p>";
    } else if (option === 'Walk') {
        infoContainer.innerHTML = "<p>Compared to an average car you are saving:<br>62.6% of CO2</p>";
    }
}