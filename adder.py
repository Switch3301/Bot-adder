from tls_client import Session
from base64 import b64encode
from json import dumps
import json
from colorama import Fore
import requests
import datetime
import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import os

os.system('cls')
cfg = json.load(open('config.json'))
locale = cfg['locale']
ua = cfg['ua']
permission = cfg['permission']
client_id  = cfg['client-id']
token = cfg['token']
captchakey  = cfg['capsolverkey']
try:
    os.system('title Bot Adder by Switch')
except:
    pass


def solve_hcaptcha():
    create_task_url = 'https://api.capsolver.com/createTask'
    get_task_result_url = 'https://api.capsolver.com/getTaskResult'
    create_task_payload = {"clientKey": captchakey,"task": {"type": "HCaptchaTaskProxyLess","websiteURL": "https://discord.com/","websiteKey": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",}}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(create_task_url, headers=headers, data=json.dumps(create_task_payload))
        if response.status_code == 200:
            result = json.loads(response.text)
            if result['errorId'] == 0:
                task_id = result['taskId']
            else:
                raise ValueError(f"Error: {result['errorDescription']}")
        else:
            raise ValueError(f"HTTP Error: {response.status_code}")
    except Exception as e:
        raise ValueError(f"Failed to create task: {str(e)}")
    status = None
    solution = None
    data = {
        "clientKey": captchakey,
        "taskId": task_id
    }
    while status != 'ready':
        time.sleep(5)
        try:
            response = requests.post(get_task_result_url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result = json.loads(response.text)
                if result['errorId'] == 0:
                    status = result['status']
                    if status == 'ready':
                        solution = result['solution']['gRecaptchaResponse']
                    else:
                        continue
                else:
                    raise ValueError(f"Error: {result['errorDescription']}")
            else:
                raise ValueError(f"HTTP Error: {response.status_code}")
        except Exception as e:
            raise ValueError(f"Failed to get task result: {str(e)}")

    return solution

thread_lock = Lock()
class Console():
    def success(message):
        Lock().acquire()
        print(f"{Fore.LIGHTGREEN_EX}[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}{Fore.RESET}")
        try:
            Lock().release()
        except:
            pass
    
    def error(message):
        Lock().acquire()
        print(f"{Fore.LIGHTBLACK_EX}[{datetime.datetime.now().strftime('%H:%M:%S')}] {Fore.LIGHTRED_EX}{message}{Fore.RESET}")
        try:
            Lock().release()
        except:
            pass

    def info(message):
        Lock().acquire()
        print(f"{Fore.LIGHTBLACK_EX}[{datetime.datetime.now().strftime('%H:%M:%S')}] {Fore.LIGHTBLUE_EX}{message}{Fore.RESET}")
        try:
            Lock().release()
        except:
            pass

    def warning(message):
        Lock().acquire()
        print(f"{Fore.LIGHTBLACK_EX}[{datetime.datetime.now().strftime('%H:%M:%S')}] {Fore.LIGHTYELLOW_EX}{message}{Fore.RESET}")
        try:
            Lock().release()
        except:
            pass
    
        
def build_num() -> str:
    response = requests.get("https://discord.com/app")
    js_version = response.text.split('"></script><script src="/assets/')[2].split('" integrity')[0]
    url = f"https://discord.com/assets/{js_version}"
    response = requests.get(url)
    build_number = response.text.split('(t="')[1].split('")?t:"")')[0]
    return build_number

try:
    build_number = int(build_num())
    Console.info(f"Scraped Build Parameter: {build_number}")
except:
    build_number = 187449
    Console.info(f"Failed to scrape build parameter, using default: {build_number}")

def get_xproperties(buildnum : int):
    return b64encode(dumps({"os":"Windows","browser":"Discord Client","release_channel":"canary","client_version":"1.0.59","os_version":"10.0.22621","os_arch":"x64","system_locale":"en-US","client_build_number":buildnum,"native_build_number":31409,"client_event_source":None,"design_id":0}).encode()).decode()

def format_locate(locale):
    locale_lang = locale.split('-')[0]
    locale = f"{locale},{locale_lang};q=0.7"
    return locale

properties  = get_xproperties(build_number)

class Adder:
    def __init__(self):
        self.session =  Session(client_identifier="chrome110")
        self.connect_headers = {
            "authority": "canary.discord.com",
            "method": "GET",
            "path": f"/api/v9/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language":  format_locate(locale),
            "authorization": token,
            "referer": "https://canary.discord.com/channels/@me",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "ua",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": locale,
            "x-super-properties": properties
            }
        url = f'https://canary.discord.com/api/v9/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands'
        self.session.get(url=url,headers=self.connect_headers)

    def add(self,server_id):
        url = f'https://canary.discord.com/api/v9/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands'
        headers = {
            "authority": "canary.discord.com",
            "method": "POST",
            "path": f"/api/v9/oauth2/authorize?client_id={client_id}&scope=bot%20applications.commands",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language":  format_locate(locale),
            "authorization": token,
            "content-type": "application/json",
            "origin": "https://canary.discord.com",
            "referer": "https://canary.discord.com/channels/@me",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": locale,
            "x-super-properties": properties
        }
        payload  = {
            'guild_id': server_id,
            'permissions': permission,
            'authorize': True
        }
        addreq = self.session.post(url=url,headers=headers,json=payload)
        if addreq.status_code == 200 and addreq.json()['location'] == 'https://discord.com/oauth2/authorized':
            Console.success(f"Added Bot to Server: {server_id} | {addreq.status_code} | No Captcha")
        elif 'captcha' in addreq.text:
            Console.warning(f"Captcha Required: {server_id} | {addreq.status_code} | Captcha")
            self.timestart = time.time()
            key = solve_hcaptcha()
            self.timeend = time.time()
            if key:
                Console.info("Solved Captcha | Key: " + key[:40] + "..."  + f" | Time: {round(self.timeend - self.timestart, 2)}s")
                payload['captcha_key'] = key
                addreq = self.session.post(url,headers=headers,json=payload)
                if addreq.status_code == 200 and addreq.json()['location'] == 'https://discord.com/oauth2/authorized':
                    Console.success(f"Added Bot to Server: {server_id} | {addreq.status_code} | Captcha")
                elif 'sitekey-secret-mismatch' in addreq.text:
                    Console.error(f"Failed to add bot to server: {server_id} |Client Error | Captcha Retrying..")
                    self.time_retry = time.time()
                    key2  = solve_hcaptcha()
                    self.timeend_retry = time.time()
                    if key2 == None:
                        return
                    else:
                        pass
                    Console.info("Solved Captcha | Key: " + key2[:40] + "..."  + f" | Time: {round(self.timeend_retry - self.time_retry, 2)}s")
                    payload['captcha_key'] = key2
                    addreq = self.session.post(url,headers=headers,json=payload)
                    if addreq.status_code == 200 and addreq.json()['location'] == 'https://discord.com/oauth2/authorized':
                        Console.success(f"Added Bot to Server: {server_id} | {addreq.status_code} | Captcha")
                    else:
                        Console.error(f"Failed to add bot to server: {server_id} | {addreq.status_code} | Captcha")
                        print(addreq.text)
                else:
                    Console.error(f"Failed to add bot to server: {server_id} | {addreq.status_code} | Captcha")
                    print(addreq.text)
        else:
            Console.error(f"Failed to add bot to server: {server_id} | {addreq.status_code}")
            print(addreq.text)


servers = open('guilds.txt','r').read().splitlines()

for i in servers:
    if len(i) < 10:
        servers.remove(i)

Console.info(f"Loaded {len(servers)} Servers!...")


def main(server_id):
    try:
        add = Adder()
        add.add(server_id  = server_id)
    except Exception as e:
        Console.error(f"Exception: | {e}")
        pass

if __name__ == '__main__':
    threads = 5
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(main, servers)
