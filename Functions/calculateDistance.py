from travelTypes import TravelType
import requests
import json


def locationToDistance(origin_lat: float, origin_long: float, dest_lat: float, dest_long: float, transport: TravelType):
    
    # Create JSON data format of origin and destination latitudes/longitute values required for the request
    data = {"origins": [
                {"waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": origin_lat,
                            "longitude": origin_long}
                    }
                }}],
            "destinations": [
                {"waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": dest_lat,
                            "longitude": dest_long}
                    }
                }}]}
    
    # Add the travel mode to the data based on the TravelType enum value passed in
    if transport == TravelType.CAR:
        data['travelMode'] = "DRIVE"
    elif transport == TravelType.BIKE:
        data['travelMode'] = "BICYCLE"
    elif transport == TravelType.WALK:
        data['travelMode'] = "WALK"
    else:
        data['travelMode'] = "TRANSIT"
    
    # Define headers needed for the API request. FieldMask indicates what data we would like to be returned.
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': 'AIzaSyCVEKGGBT_8WryClHT64tPqFONldHdY35Y',
        'X-Goog-FieldMask': 'distanceMeters,condition'
    }

    # Carry out the post request and check if the status code is a success. If not, handle the error accordingly and return 0 to indicate failure
    response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=data, headers=headers)
    if response.status_code != 200:
        print(f"Error {response.status_code} whilst computing route matrix: {response.reason}")
        result = json.loads(response.text)
        print(f"Status: {data[0]['error']['status']}\nMessage: {data[0]['error']['message']}")
        return 0
    
    # Convert text response to JSON and return distance in metres, or 0 if no valid results returned
    result = json.loads(response.text)
    if len(result) > 0:
        if result[0]['condition'] == "ROUTE_EXISTS":
            return result[0]['distanceMeters']
    return 0


# Test function
print(locationToDistance(50.727163, -3.535225, 50.736235, -3.534693, TravelType.BIKE))