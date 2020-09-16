import nfc
import time
import platform
import os
import sys
import requests
import datetime
import json
from nfc.clf import RemoteTarget
from dotenv import load_dotenv
from datetime import datetime

try:
    from pitftgpio import PiTFT_GPIO
except ImportError:
    # Do nothing as we can't import the PiTFT_GPIO package when we're
    # running on Windows.
    x = 0

# Load environment variables in .env.
load_dotenv()

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def clear():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

# Clear the screen and setup the TFT screen GPIO buttons.
clear()
pitft = None

if platform.system().lower() != 'windows':
    PiTFT_GPIO()

# Setup the NFC reader.
try:
    clf = nfc.ContactlessFrontend('usb')
except IOError:
    print('ERROR: Could not find reader.')
    sys.exit(-1)

# Set some variables used here.
id = None
idVal = ''
bl = True

while True:
    if pitft != None:
        if pitft.Button1: # Make it possible to dim/brighten the TFT screen.
            bl ^= bl
            pitft.Backlight(bl)
            print('Backlight Toggle')
            time.sleep(2.0)
            clear()

        if pitft.Button2: # Let's provide a physical means from breaking out of the loop.
            print('Quitting')
            sys.exit(0)

    # Define the target tags we want to read and look for them.
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    
    if target is not None:
        if target.sdd_res != id: # Check if tag has changed, as we don't want a user tagging-in causes multiple cycles.
            try:
                # Read the tag and assign the UID to the appropriate variables.
                tag = nfc.tag.activate(clf, target)
                id = target.sdd_res
                idVal = id.hex()

                # Get the URL to send the call to.
                url = os.getenv("WEBHOOK_URL")

                # Why do I append 9000 to the UID of the tag? Because the RC-S380 in Windows if using the .NET
                # Framework Library for it adds the extra bytes to the array. As such, if we need to use the tag's
                # UID for other things, then we need to make sure that the UIDs are consistent.
                data = json.dumps(
                { 
                    'cardNumber': f'{idVal}9000'.upper(), 
                    'timestamp': datetime.datetime.now() 
                }, default = default)

                # Let it rip...
                requests.post(url, data = data)

                print('')
                print('')
                print('  ██████  ██   ██ ██ ')
                print(' ██    ██ ██  ██  ██ ')
                print(' ██    ██ █████   ██ ')
                print(' ██    ██ ██  ██     ')
                print('  ██████  ██   ██ ██ ')
                
            except ConnectionError:
                print('')
                print('')
                print(' ██   ██  ██████  ██   ██  ')
                print(' ██   ██ ██  ████ ██   ██  ')
                print(' ███████ ██ ██ ██ ███████  ')
                print('      ██ ████  ██      ██  ')
                print('      ██  ██████       ██  ')

            except Exception as err:
                diag_url = os.getenv("DIAGNOSTIC_URL")
                if diag_url != None:
                    requests.post(diag_url, data = json.dumps(
                    {
                        'tag_id': idVal,
                        'timestamp': datetime.now(),
                        'error': err
                    }))

                print('')
                print('')
                print(' ███████  █████  ██ ██      ')
                print(' ██      ██   ██ ██ ██      ')
                print(' █████   ███████ ██ ██      ')
                print(' ██      ██   ██ ██ ██      ')
                print(' ██      ██   ██ ██ ███████ ')

    elif target is None and id != '': # We've most likely taken the tag away.
        clear()
    
    # Give us some time for the user to know that it either
    # succeeded or failed.
    time.sleep(0.25)