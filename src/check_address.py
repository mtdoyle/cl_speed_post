import time
import re
import requests

def get_speed(address):
    address_to_send = address.split(",")[0:2]
    house_num = address_to_send[0].split()[0]
    street_name = address_to_send[0].split()[1]
    street_type = address_to_send[0].split()[2]
    print("Checking address {0}".format(address_to_send))
    response = requests.post(
        "https://shop.centurylink.com/MasterWebPortal/freeRange/login/shop/addressAuthentication?form.authType=ban&form.newShopAddress=true&form.pageType=page&form.singleLineAddress={0}+{1}+{2},{3},MN,USA&form.unitNumber=".format(house_num, street_name, street_type, address_to_send[1]),
        verify=False)

    page_source = response.text
    found_speeds = re.findall("thisProd\['downDisplay'\].*", page_source)
    highest_speed = 0
    for speed in found_speeds:
        curr_speed = float(re.sub(r'[a-zA-Z\'\[\]\"\;=\s]+', r'', speed))
        if curr_speed > highest_speed:
            highest_speed = curr_speed
    print("Highest speed found: {0} Mbps".format(highest_speed))
    return highest_speed