def convert24(str1: str) -> float:

    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:].upper() == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:].upper() == "AM":
        return str1[:-2]

    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:].upper() == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:
        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:-2]


def lat_long_difference(coord1:tuple,coord2:tuple):
    import geopy.distance
    return round(geopy.distance.geodesic(coord1, coord2).km,2)

if __name__ == '__main__':
    print(convert24("10:08pm"))
