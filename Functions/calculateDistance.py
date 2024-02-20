from travelTypes import TravelType
import requests

# API Key: AIzaSyBaD5ewdHFDtDg6gPGxehsW6dUpsKtEBeo

def locationToDistance(origin: str, dest: str, transport: TravelType):
    data = {"origins": [
                {"waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": 50.727163,
                            "longitude": -3.535225}
                    }
                }}],
            "destinations": [
                {"waypoint": {
                    "location": {
                        "latLng": {
                            "latitude": 50.736235,
                            "longitude": -3.534693}
                    }
                }}],
                "travelMode": "DRIVE"}
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': 'AIzaSyCVEKGGBT_8WryClHT64tPqFONldHdY35Y',
        'X-Goog-FieldMask': 'originIndex,destinationIndex,duration,distanceMeters,status,condition'
    }
    
    response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=data, headers=headers)
    print(response)
    print(response.text)


locationToDistance(1,2,3)