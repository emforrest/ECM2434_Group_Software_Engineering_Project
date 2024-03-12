
"""Defines an enum that maps travel methods to their CO2 emissions per KM.

The Enum is to be used to standarise how we refer to travel methods throughout
the Django app. Figures used are taken from the following sources: 
- https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/901692/conversion-factors-2020-methodology.pdf
- https://ecf.com/news-and-events/news/how-much-co2-does-cycling-really-save

Authors:
- Sam Townley
- Jack Skinner
"""

from enum import Enum

class TravelType(Enum):
    """Enum defining the CO2 emissions per KM for different modes of transport.
    
    Defined to help standardise references to modes of transport throughout the
    Django app. Has methods to convert these easily to/from human readable
    strings.

    Attributes:
        CAR (float): CO2 emissions per KM for an average diesel car.
        BUS (float): CO2 emissions per KM for an average bus journey.
        TRAIN (float): CO2 emissions per KM for an average train journey.
        BIKE (float): CO2 emissions per KM when cycling.
        WALK (float): CO2 emissions per KM when walking.
    """
    CAR = 0.15
    BUS = 0.10
    TRAIN = 0.041
    BIKE = 0.021
    WALK = 0.056
    
    def __str__(self) -> str:
        """Overwrites the default values returned from str(TravelType).

        Returns:
            str: A simplified string representation of the enum.
        """
        if self.name == "CAR":
            return "car"
        elif self.name == "BUS":
            return "bus"
        elif self.name == "TRAIN":
            return "train"
        elif self.name == "BIKE":
            return "bike"
        else:
            return "walk"
        
    @staticmethod
    def from_str(string: str) -> Enum:
        """Returns a TravelType enum based on the string passed in.

        Args:
            string (str): The travel method in a string format.

        Returns:
            Enum: A TravelType enum mapping to the string argument.
        """
        if string.lower() in ["bus", "by bus", "using the bus"]:
            return TravelType.BUS
        elif string.lower() in ["train", "by train", "using the train"]:
            return TravelType.TRAIN
        elif string.lower() in ["bike", "cycling", "by bike"]:
            return TravelType.BIKE
        elif string.lower() in ["walk", "walking", "on foot"]:
            return TravelType.WALK
        elif string.lower() in ["car", "driving", "by car"]:
            return TravelType.CAR
        else:
            return None
        
    
    def to_str(self) -> str:
        """Gives a morereadable version that can be used within the frontend.
        
        Similar to overwriting the "toString()" method in Java.

        Returns:
            str: A human readable string version of the enum name.
        """
        if self.name == "CAR":
            return "driving"
        elif self.name == "BUS":
            return "using the bus"
        elif self.name == "TRAIN":
            return "using the train"
        elif self.name == "BIKE":
            return "cycling"
        else:
            return "walking"