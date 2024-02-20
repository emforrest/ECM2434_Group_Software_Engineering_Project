#These are the functions for calculating how much CO2 has been saved by the journey being done sustainably

#figures from https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/901692/conversion-factors-2020-methodology.pdf
#and https://ecf.com/news-and-events/news/how-much-co2-does-cycling-really-save

#Declare constants for CO2 emmissions per kiliometer to 3sf

CAR = 0.15
BUS = 0.10
TRAIN = 0.041
BIKE = 0.021
WALK = 0.056

#function takes in distance traveled, and a number representing how they did it. web app will call this fuction.
def distanceToCO2(distance, transport):
        match transport: 
                case 0: 
                        transport = BUS 
                case 1:   
                        transport = TRAIN
                case 2: 
                        transport = BIKE 
                case 3: 
                        transport = WALK 
        co2_saved = distance * abs(transport - CAR)
        return co2_saved 
