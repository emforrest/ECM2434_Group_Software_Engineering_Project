
from enum import Enum

# figures from https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/901692/conversion-factors-2020-methodology.pdf
# and https://ecf.com/news-and-events/news/how-much-co2-does-cycling-really-save

# Declare enum mapping travel types to CO2 emmissions per kiliometer (to 3sf)
# This way it can be imported and use to standardize travel types across the backend

class TravelType(Enum):
    CAR = 0.15
    BUS = 0.10
    TRAIN = 0.041
    BIKE = 0.021
    WALK = 0.056
    
    def __str__(self) -> str:
        if self.name == "CAR":
            return "Driving"
        elif self.name == "BUS":
            return "By bus"
        elif self.name == "TRAIN":
            return "By train"
        elif self.name == "BIKE":
            return "Cycling"
        else:
            return "Walking"
        
    @staticmethod
    def from_str(string: str) -> Enum:
        if string.lower() in ["bus", "by bus"]:
            return TravelType.BUS
        elif string.lower() in ["train", "by train"]:
            return TravelType.TRAIN
        elif string.lower() in ["bike", "cycling", "by bike"]:
            return TravelType.BIKE
        elif string.lower() in ["walk", "walking", "on foot"]:
            return TravelType.WALK
        elif string.lower() in ["car", "driving", "by car"]:
            return TravelType.CAR
        else:
            return None