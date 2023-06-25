from os import name, system
import threading
import time
def install(package):
    os.system(f"pip install {package}")

# Check if grpc is installed
try:
    import grpc
except ImportError:
    print("grpc library not found. Installing...")
    install('grpcio')

# Check if requests is installed
try:
    import requests
except ImportError:
    print("requests library not found. Installing...")
    install('requests')

# Check if protobuf is installed
try:
    import google.protobuf
except ImportError:
    print("protobuf library not found. Installing...")
    install('protobuf')

import grpc
import random
import string
import snapchat_activation_api_pb2
import snapchat_activation_api_pb2_grpc
import requests
import json
import os

class CheckUsername:
    def __init__(self, length=4,sleep=0.5):
        self.server_address = 'aws.api.snapchat.com'
        self.server_port = 443
        self.length = length
        self.sleep = sleep
        self.done = 0
        self.taken = 0
        self.band = 0

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def send_message_to_telegram_bot(self, username):
        try:
            with open('bot.json') as file:
                bot_data = json.load(file)

            bot_token = bot_data.get('token')
            chat_id = bot_data.get('chat_id')
        except:
            bot_token, chat_id = None, None
        if not bot_token or not chat_id:
            return

        message = f"""
[ ! ] Done Get User Sir .
[ ! ] Attempts  : {self.done + self.taken + self.band}
[ ! ] Username : {username}

- By Kings  @givtt | @ifostn
"""
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": message
        }
        requests.get(url, params=params)

    def generate_random_username(self):
        length = self.length
        username = random.choice(string.ascii_lowercase)
        characters = string.ascii_letters  + "_-"
        username += ''.join(random.choice(characters) for _ in range(length - 2))
        username += random.choice(string.ascii_letters + string.digits)
        username = username.replace("__", "_").replace("--", "-")
        return username.lower()


    def check_username_availability(self, username):
        channel = grpc.secure_channel(
            f'{self.server_address}:{self.server_port}',
            grpc.ssl_channel_credentials()
        )
        stub = snapchat_activation_api_pb2_grpc.SuggestUsernameServiceStub(channel)

        metadata = [('allow-recycled-username', 'true')]
        request = snapchat_activation_api_pb2.CheckUsernameRequest(
            ww=username,
            unused=0,
            request_id='e8a22d8d-c83d-2c58-aabb-7e55f1b546f8',
            session_id='8d38652e-c6a3-5fad-48ae-6f601802bb4d'
        )
        response = stub.CheckUsername(request, metadata=metadata)

        channel.close()  # Close the gRPC channel after the request
        
        return response

    def check_username(self, username):
        print(f"\r[ Done ] : {self.done}  | [ Taken ] : {self.taken}  | [ Band ] : {self.band} | [ User ] : {username}", flush=True, end='')
        try:
            response = self.check_username_availability(username)
            is_available = response.is_available
            
            if is_available == 1:
                self.done +=1
                with open('Available.txt', 'a') as file:
                    file.write(username + '\n')
                self.send_message_to_telegram_bot(username)
            else:
                self.taken +=1

        except Exception as e:
            self.band +=1

    def check_usernames_concurrently(self, usernames):
        threads = []
        for username in usernames:
            thread = threading.Thread(target=self.check_username, args=(username,))
            thread.start()
            threads.append(thread)
            time.sleep(self.sleep)  
        for thread in threads:
            thread.join()

    def check_usernames_from_file(self, filename):
        filename = str(filename).replace(" ",'').replace('"','')
        try:
            with open(filename, 'r') as file:
                usernames = [line.strip() for line in file.readlines()]
                self.check_usernames_concurrently(usernames)
        except FileNotFoundError:
            print("[X] File not found.")

print("""

                 ,  ,
              #▄▓██████▀
            "▀███████████▄L
           ▄R████████████▄▄
            ▄▀█████████▓▀▀N
             ' ▀█▀███▀█ ▀
                ' ▀█▌"
                   ▐█
                   ██
                   ██
    ""▀▀▀██▄▄   ▄▄▄██▄a▄▄   ,▄▄██▀▀""
           "▀██▄⌠▀▀▀▀▀'¡▄██▀"
               ▀██▄  ▄██▀`
                  ████"
               ▄▄█▌▀╙██▄▄
          ██▄▄██▀█    █▀███▀█▌

     [ Made By GIVT & f09l ]
     [ + ] Telegram  :  @givtt
     [ + ] Instagram :  @we62
     
     [ + ] Telegram  :  @ifostn
     [ + ] Instagram :  @f09l
     
     [ ! ] You are not entitled to sell the Tool [ ! ]
""")
time.sleep(2)
CheckUsername().clear()

while True:
    option = input("[/] Choose an option:\n[1] Generate and check random usernames\n[2] Check usernames from a file\n[E] Exit\n[?] Enter: ")

    if option == "1":
        while True:
            try:
                length = int(input("[?] Enter usernames length: "))
                count = int(input("[?] Enter number of usernames to check: "))
                sleep = float(input("[?] Sleep: "))
                break
            except ValueError:
                print("[X] Invalid input. Please enter a valid integer.")
        CheckUsername().clear()
        check = CheckUsername(length,sleep=sleep)
        usernames = [check.generate_random_username() for _ in range(count)]
        check.check_usernames_concurrently(usernames)

    elif option == "2":
        filename = str(input("[?] Enter the filename: ")).replace(' ','').replace("'",'').replace('"','')
        try:
            sleep = float(input("[?] Sleep : "))
            CheckUsername().clear()
        except:
            sleep = 0.5
        check = CheckUsername(sleep=sleep)
        check.check_usernames_from_file(filename)

    elif option == "E":
        exit("Exit")

    else:
        print("[X] Invalid option. Please choose a valid option.")
