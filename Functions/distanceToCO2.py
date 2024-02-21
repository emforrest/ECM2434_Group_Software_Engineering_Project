# These are the functions for calculating how much CO2 has been saved by the journey being done sustainably
from travelTypes import TravelType

#function takes in distance traveled, and a number representing how they did it. web app will call this fuction.
def distanceToCO2(distance, transport):
        match transport: 
                case 0: 
                        transport = TravelType.BUS 
                case 1:   
                        transport = TravelType.TRAIN
                case 2: 
                        transport = TravelType.BIKE 
                case 3: 
                        transport = TravelType.WALK 
        co2_saved = distance * abs(transport - TravelType.CAR)
        return co2_saved 
