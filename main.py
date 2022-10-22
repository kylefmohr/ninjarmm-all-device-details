import ninjarmm_api
import json, time

client_id = input("Enter your legacy API client ID: ")
client_secret = input("Enter your legacy API secret: ")
filename = input("Name for the output JSON file: ")
highest_id = int(input("Enter the most recently registered device ID: "))
eu = input("Are you in the EU? (y/n): ")
verbose = input("Verbose output? (y/n): ")
if eu == "y":
    eu = True
else:
    eu = False
if verbose == "y":
    debug_choice = True
else:
    debug_choice = False

ninja = ninjarmm_api.client(client_id, client_secret, iseu=eu, debug=debug_choice)

outfile = filename
api_limit = 10
api_timeout = 60

rate_limited = False
finished = False
current_device = 1  # the device ID to start with. Adjust this if you want to resume a previous run

# append to outfile
with open(outfile, "a") as f:
    while not finished:
        while not rate_limited:
            for i in range(current_device, highest_id, 1):
                current_device = i+1
                print(i)
                f.write(str(i))
                f.write("\n----------------------------------------------------------------------------------------------------------------------------\n")
                computer_json_info = ninja.get_device(i)
                computer_string_info = json.dumps(computer_json_info, indent=4)
                if computer_string_info.find("Request rate limit exceeded") != -1:
                    rate_limited = True
                    print("Got bad response, breaking")
                    break
                if verbose:
                    print(json.dumps(computer_json_info, indent=4, sort_keys=True))
                    print("\n----------------------------------------------------------------------------------------------------------------------------\n")
                f.write(json.dumps(computer_json_info, indent=4, sort_keys=True))
                f.write("\n----------------------------------------------------------------------------------------------------------------------------\n")
                time.sleep(1)
                if i % api_limit == 0:
                    rate_limited = True
                    print("Rate limited, breaking")
                    break
            break

        while rate_limited:
            for i in range(api_timeout, 0, -1):
                if verbose:
                    print(i)
                time.sleep(1)
            rate_limited = False
            print("Resuming")
