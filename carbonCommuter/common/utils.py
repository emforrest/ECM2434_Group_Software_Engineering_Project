
"""A module defining common utility functions to be used throughout the Django app

These functions often relate to generic functionality not related to Django users
or the web requests themselves, or for functions which interface with external
files such as campusCoordinates.json

Authors:    
- Sam Townley
- Jack Skinner
"""

import json
import math
import requests
from typing import Union
from datetime import datetime
from common.travelTypes import TravelType
from leaderboard.models import Leaderboard_Entry


def calculate_co2(distance: float, transport: TravelType|str) -> float:
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
    
    # Verify method of transport is valid and return CO2 savings to 2 d.p
    if type(transport) is TravelType and transport is not None:
        savings = distance * abs(TravelType.CAR.value - transport.value)
        return round(savings, 2)
    else:
        raise ValueError("Unknown mode of transport specified!")


def get_route(origin_lat: float, origin_long: float, dest_lat: float, dest_long: float, transport: TravelType) -> Union[float, float]:
    """Calculates the distance and time between 2 locations using the Google Maps API.
    
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
        float: The expected time the journey would usually take (not accounting for traffic).
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
        'X-Goog-FieldMask': 'distanceMeters,condition,staticDuration'
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
            distance = result[0]['distanceMeters'] / 1000
            duration = float(result[0]['staticDuration'].replace("s", "")) / 60
            return distance, duration
    return 0, 0
    
    
def load_campus_coords() -> dict:
    """Loads the campus locations and their coordinates from the stored json file.

    Returns:
        dict: A dictionary of locations with latitude and longitude values inside.
    """
    # Load campus coords from json file
    with open("common/campusCoordinates.json", "rb") as file:
        campus = json.load(file)
        file.close()
    return campus


def calculate_direct_distance(location1: tuple | Union[float, float], location2: tuple | Union[float, float]) -> float:
    """Calculates the stright line distance between two geocoded locations.
    
    Designed for checking proximity of 2 locations to each other.

    Args:
        location1 (tuple): A tuple containing the latitude and longitude of the origin location.
        location2 (tuple): A tuple containing the latitude and longitude of the destination.

    Returns:
        float: The straight line distance measured in KM.
    """
    # Define the number of degrees in each KM (calculated as 360 divided by the circumference of earth)
    DEGREES_PER_KM = 0.00898315277071498185515429725208
    
    # Use Pythagorean theorem to calculate the magnitude of the straight line distance between two co-ordinates (latitude and longitude).
    distance = math.sqrt(math.pow((location1[0] - location2[0]), 2) + math.pow((location1[1] - location2[1]), 2)) / DEGREES_PER_KM
    return distance


def get_distance_to_campus(lat: float, lng: float) -> Union[str, float]:
    """Gets the name and distance to the closest building on campus based on the given latitude and longitude.

    Args:
        lat (float): The current latitude of the user.
        lng (float): The current longitude of the user.
        
    Returns:
        str: The name of building on campus, as saved in the database and inside campusCoordinates.json
        float: The distance to the marked building location, measured in KM.
    """
    # Load the stored locations on campus from the local JSON file.
    campus = load_campus_coords()
    
    # Create a dictionary of distances for each location to the users location.
    results = {}
    for name, coords in campus.items():
        distance = calculate_direct_distance((lat, lng), (coords["latitude"], coords['longitude']))
        results[name] = distance
    
    # Order the dictionary, and return the top key pair.
    ordered = dict(sorted(results.items(), key=lambda item: item[1]))
    return list(ordered.items())[0]


def format_time_between(time1: datetime, time2: datetime) -> str:
    """Formats the timedelta between two datetimes into a human-readable string.

    Args:
        time1 (datetime): The start datetime.
        time2 (datetime): The end datetime.

    Returns:
        str: A formatted representation of time difference.
    """
    # Calculate the hours and minutes between the two datetimes
    diff = time1 - time2
    hours = diff.days * 24 + diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    # If 1 or more hours, add this to the result string.
    formatted = ""
    if hours > 1:
        formatted += f"{hours} hours"
    elif hours == 1:
        formatted += "1 hour"
        
    # If both hours and minutes are present, add an ampersand between the two.
    if hours > 0 and minutes > 0:
        formatted += " & "
    
    # Add the minutes to the string if there are any.
    if minutes > 1:
        formatted += f"{minutes} minutes"
    else:
        formatted += "1 minute"
    return formatted

def leaderboardData(users_journeys):
    users = []
    current_id = -1
    for journey in users_journeys:
        print(journey.user_id)
        if journey.user.id != current_id: 
            if current_id != -1:
                users.append(user_entry)
            user_entry = Leaderboard_Entry()
            current_id = journey.user_id
            user_entry.name = journey.user.first_name + " " + journey.user.last_name
            user_entry.totalCo2Saved = 0
        try:
            user_entry.totalCo2Saved += journey.carbon_savings
        except:
            user_entry.totalCo2Saved += 0
    users.append(user_entry)
    users.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users = users[:10]
    for x in range(0,len(users)):
        users[x].position = x+1
    return users