from travelTypes import TravelType
import requests

# API Key: AIzaSyBaD5ewdHFDtDg6gPGxehsW6dUpsKtEBeo

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
    
    response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=data, headers=headers)
    print(response)
    print(response.text)


locationToDistance(50.727163, -3.535225, 50.736235, -3.534693, TravelType.CAR)