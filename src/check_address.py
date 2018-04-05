import time
import re
import requests
import json

def get_speed(address):
    address_to_send = address.split(",")[0:2]
    print("Checking address {0}".format(address_to_send))
    submit_string = address_to_send[0].replace(' ', '+')
    response = requests.post(
        "https://shop.centurylink.com/MasterWebPortal/freeRange/login/shop/addressAuthentication?form.authType=ban&form.newShopAddress=true&form.pageType=page&form.singleLineAddress={0},{1},MN,USA&form.unitNumber=".format(submit_string, address_to_send[1]),
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