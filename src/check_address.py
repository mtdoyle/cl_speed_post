import time
import re
import requests
import json

def get_speed(address):
    address_to_send = address.split(",")[0:2]
    raw_response = requests.get("https://geoamsrvcl.centurylink.com/geoam/addressmatch/addresses?q={0},{1}".format(address_to_send[0],address_to_send[1]), verify=False).text
    json_response = json.loads(raw_response)
    if json_response['responseData']['addresses']:
        submit_string = json_response['responseData']['addresses'][0]['fullAddress'].replace(' ', "+")
    else:
        print("Bad address: {0}".format(address_to_send))
        return "0.5"
    print("Checking address {0}".format(address_to_send))
    response = requests.post(
        "https://shop.centurylink.com/MasterWebPortal/freeRange/login/shop/addressAuthentication?form.authType=ban&form.newShopAddress=true&form.pageType=page&form.singleLineAddress={0}&form.unitNumber=".format(submit_string),
        verify=False)

    page_source = response.text
    found_speeds = re.findall("thisProd\['downDisplay'\].*", page_source)
    highest_speed = 0
    curr_speed = None
    for speed in found_speeds:
        if "768" in speed:
            speed = "0.768"
        try:
            curr_speed = float(re.sub(r'[a-zA-Z\'\[\]\"\;=\s]+', r'', speed))
        except Exception as e:
            print(e)
            return 0
        if curr_speed is None:
            return 0
        elif curr_speed > highest_speed:
            highest_speed = curr_speed
    print("Highest speed found: {0} Mbps".format(highest_speed))
    return highest_speed