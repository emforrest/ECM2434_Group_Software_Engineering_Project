
"""A module defining common utility functions to be used throughout the Django app

These functions often relate to generic functionality not related to Django users
or the web requests themselves, or for functions which interface with external
files such as campusCoordinates.json

Authors:    
- Sam Townley
- Jack Skinner
"""

import json
import requests
from common.travelTypes import TravelType

def distanceToCO2(distance: float, transport: TravelType|str) -> float:
    """Calculates the CO2 compared to driving based on the distance travelled.

    Args:
        distance (float): The distance travelled, measured in KM.
        transport (TravelType | str): The method of transport used.
        
    Raises:
        ValueError: One or more arguments is invalid.

    Returns:
        float: The CO2 emissions saved by the journey compared to driving.
    """
    # Verify distance is non-negative
    if distance < 0:
        raise ValueError("Distance must be non-negative!")
    
    # If transport is specified as a string, convert it to a TravelType first.
    if type(transport) is str:
        transport = TravelType.from_str(transport)
    
    # Verify method of transport is valid
    if type(transport) is TravelType and transport is not None:
        return distance * abs(TravelType.CAR.value - transport.value)
    else:
        raise ValueError("Unknown mode of transport specified!")


def locationToDistance(origin_lat: float, origin_long: float, dest_lat: float, dest_long: float, transport: TravelType) -> float:
    """Calculates the distance between 2 locations using the Google Maps API.
    
    Uses the Google Maps Places API endpoint to estimate the distance travelled
    between 2 points using the most efficient route as generated by Google. This
    takes into account the mode of transport used as well.
    
    Args:
        origin_lat (float): The latitude, in degrees, of the origin (between -90 and 90).
        origin_long (float): The longitude, in degrees, of the origin (between -180 and 180).
        dest_lat (float): The latitude, in degrees, of the destination (between -90 and 90).
        dest_long (float): The longitude, in degrees, of the destination (between -180 and 180).
        transport (TravelType): The method of transport used to make the journey.

    Raises:
        ValueError: One or more of the latitude/longitude parameters are invalid.
        RuntimeError: An unknown error occured during the API call.

    Returns:
        float: The distance calculated, given in metres.
    """
    
    # Verify origin and destination latitude/longitude coordinates are within the valid range
    if abs(origin_lat) > 90:
        raise ValueError(f"Origin's latitude '{origin_lat}' is outside the maximum range of -90 to 90!")
    elif abs(dest_lat) > 90:
        raise ValueError(f"Destination's latitude '{dest_lat}' is outside the maximum range of -90 to 90!")
    elif abs(origin_long) > 180:
        raise ValueError(f"Origin's longitude '{origin_long}' is outside the maximum range of -180 to 180!")
    elif abs(dest_long) > 180:
        raise ValueError(f"Destination's longitude '{dest_long}' is outside the maximum range of -180 to 180!")
    
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
        raise RuntimeError(f"Error {response.status_code} whilst computing route matrix: {response.reason}")
    
    # Convert text response to JSON and return distance in metres, or 0 if no valid results returned
    result = json.loads(response.text)
    if len(result) > 0:
        if result[0]['condition'] == "ROUTE_EXISTS":
            return result[0]['distanceMeters']
    return 0


def getCampusCoords(location: str) -> dict:
    """Returns the longitude and latitude coordinates of locations on campus
    
    Loads the locations defined in campusCoordinates.json and returns the 
    dictionary containing latitude and longitude coordinates if a mapping
    exists with a matching key.

    Args:
        location (str): The location name on campus as given in campusCoordinates.json.

    Raises:
        ValueError: Location on campus doesn't have a lat/long mapped to it.

    Returns:
        dict: A dictionary with 2 keys, latitude and longitude containing float values.
    """
    
    # Load campus coords from json file
    with open("common/campusCoordinates.json", "rb") as file:
        campus = json.load(file)
        file.close()
    
    # Return latitude and longitude dictionary associated with location name in file
    if location in campus.keys():
        return campus[location]
    else:
        raise ValueError("Unknown location on campus!")
