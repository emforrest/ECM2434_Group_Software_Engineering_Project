
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