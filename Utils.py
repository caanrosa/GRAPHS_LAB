from termcolor import colored
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    
    R = 6373.0  # Radio de la Tierra en km
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine (Una fórmula ahí que vi en Stack Overflow :v)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

def printTitle(title, centerNum=64):
    print (colored(f" {title} ".center(centerNum, "⸺"), "red"))
    
def printSubtitle(subtitle, centerNum=64):
    print (colored(f" {subtitle} ".center(centerNum), "light_grey"))
    
def printOption(number, option, colorNumber="red", colorOption="white"):
    op = colored(f" ({number})", colorNumber) + colored(f" {option} ", colorOption)
    
    print (f"{op}".center(80))
    
def printBottom():
    print (colored("".center(64, "⸺"), "red"))
             
    
def getInput() -> str:
    got = ""
    while(len(got) == 0):
        got = input(colored("> ", "green"))
        
    return got

def getInputInt() -> int:
    recieved = ""
    p = False
    
    while(not p):
        recieved = getInput()
        try:
            int(recieved)
            p = True
        except ValueError:
            p = False
    
    return int(recieved)