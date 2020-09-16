# covid-checkin
A Python script for creating a NFC driven employee check-in point of presence for use during the SARS-Cov-2 (COVID-19) pandemic.

# About this project
The need to create this script arose with the nature of my workplace, given that my employer is extremely understanding of fact that not all employees wanted to return to the office while the pandemic was still happening. As such, we felt that it was important to create a means for employees who may be either occasional users of the office space or wanted to return on a more permanent basis to identify when they were in the building. 

The coivd-checkin script connects and sends a message to a webhook service which then integrates with a Google Forms survey that employees must complete prior to entering the office. If the employee fails to complete the survey prior to "tagging-in" or if they indicated in the survey that they may have symptoms matching the list of symptoms provided by the Government of Ontario used in screening for SARS-Cov-2, they and their manager would be notified when they "tag-in". The repository contains solely the python script used to read an NFC tag's UID and send it along with the current timestamp to a URL provided in a .env file.

The project is provided as-is so that others may use the script to create either their own versions and maybe to better understand how they can adopt their own policies in their offices. The intent is not to provide a surveilence tool, but something to help people ensure compliance with their jursidiction's rules and to help ensure the safety of their coworkers.

# Requirements
- A Raspberry Pi (3B+ or better).
- A NFC reader. The Sony RC-S380 is recommended.
  *You should be able to use any NFC reader listed in the nfcpy library's documentation.*
- A WiFi or Ethernet Connection.
- A webhook service to send the NFC tag's UID to.

## Optional Requirements
- The Adafruit 2.8" TFT Touchscreen (or similar) PiHat.

# Instructions
- Clone the repository.
- Run `pip3 install -U nfcpy requests python-dotenv`
- Setup your .env file, specifying the WEBHOOK_URL to call.
- If you have the Adafruit TFT PiHat attached, set the pin values for the buttons that correspond to your model.
- Run the script.

If you're on windows, you'll need to install libusb. You can follow the instructions here: https://nfcpy.readthedocs.io/en/latest/topics/get-started.html.
