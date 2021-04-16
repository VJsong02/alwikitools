import requests
import json
import os
from getpass import getpass
from time import sleep

s = requests.Session()
token = ""

def login():
    url = "https://azurlane.koumakan.jp/w/api.php?action=query&meta=tokens&type=login&format=json"
    response = json.loads(s.get(url).content.decode())
    token = response['query']['tokens']['logintoken']
    print("Token acquired:", token)

    url = "https://azurlane.koumakan.jp/w/api.php?action=clientlogin&format=json"
    
    username = password = ""
    if os.path.exists("config"):
        with open("config") as f:
            l = f.read().strip().split("\n")
            username, password = l
            print("Logging in as", username)
    else:
        username = input("Username: ")
        password = getpass()
        open("config", "w").write(f"{username}\n{password}")
        
    post = {
        "username": username, 
        "password": password,
        "logintoken": token,
        "loginreturnurl": "https://azurlane.koumakan.jp/"
    }
    response = json.loads(s.post(url, post).content.decode())
    print("Login:", response['clientlogin']['status'])
    if response['clientlogin']['status'] != "PASS":
        os.remove("config")
        print(response)

    url = "https://azurlane.koumakan.jp/w/api.php?action=query&meta=tokens&format=json"
    response = json.loads(s.get(url).content.decode())
    token = response['query']['tokens']['csrftoken']
    print("csrf token:", token)
    
    return token

d = "./input/"
url = "https://azurlane.koumakan.jp/w/api.php?action=upload&format=json"
while True:
    print(d, "> ", end="")
    c = input().split()
    
    if c[0] == "upload":
        for f in os.listdir(d):
            file = open(d + f, "rb")
            print("Uploading", d, f, "...", end=" ")
            files = {"file" : (f, file, 'multipart/form-data')}
            post = {
                "filename" : f,
                "token" : token,
                "comment" : "Uploaded by VJsong03"
            }
            response = s.post(url, files=files, data=post).content.decode()
            file.close()
            print(json.loads(response)['upload']['result'])
            if json.loads(response)['upload']['result'] != "Success":
                print(json.loads(response))
            
    elif c[0] == "login":
        token = login()
    
    elif c[0] == "setdir":
        d = " ".join(c[1:])
            
    elif c[0] == "quit":
        print("Bye")
        break