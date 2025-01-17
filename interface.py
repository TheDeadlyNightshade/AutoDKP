# interfaces with WebDKP by mimicing the website's internal API

import common
import requests
import ast
import json

# mapping from player IDs to names
player_id_to_name = {common.player_info[k]["id"]: k for k in common.player_info}


# utility function to send a DKP table edit request, used by the other API funtcions
def send(pool, data):
    print("Sending data to pool:", pool)
    print("Common table IDs:", common.table_ids)
    r = requests.post(url=common.url + "/Admin/Manage" + "&t=" + str(common.table_ids[pool]), headers=common.headers,
                      data=data)
    return r.json()[0], r.json()[1]


# command: sync the player info
def sync_players():
    new_player_info = {}
    for pool in common.table_ids:
        page_number = 1
        empty = False
        while not empty:
            html = requests.get(
                f"{common.url}/{page_number}?t={common.table_ids[pool]}"
            ).content.decode()
            empty = True
            for line in html.split("\n"):
                if line.startswith("table.Add({"):
                    empty = False
                    try:
                        data = json.loads(line[line.find("{"):line.find("}") + 1])
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}")
                        continue  # Skip this iteration

                    player_name = data.get("player")
                    if player_name and player_name not in new_player_info:
                        new_player_info[player_name] = {
                            "id": data.get("userid"),
                            "class": data.get("playerclass"),
                            "clan": data.get("playerguild") if data.get("playerguild") is not None else "No Guild",
                            "dkp": {}
                        }
                    if player_name:
                        # Ensure pool exists in "dkp" dictionary
                        new_player_info[player_name]["dkp"].setdefault(pool, {})
                        new_player_info[player_name]["dkp"][pool] = data.get("dkp", 0)
            page_number += 1

    common.player_info = new_player_info


# command: set the raw dkp points of a player
def force_dkp(player, amount, pool):
    if player not in common.player_info:
        return False, "Player does not exist"
    data = {
        "ajax": "EditPlayer",
        "id": common.player_info[player]["id"],
        "name": player,
        "guild": common.clan,
        "playerclass": common.player_info[player]["class"],
        "dkp": amount
    }
    return send(pool, data)


# command: award DKP to players, such as via a boss kill
def award_dkp(players, reason, amount, pool):
    try:
        ids = [str(common.player_info[p]["id"]) for p in players]
    except KeyError:
        return False, "At least one player in the list does not exist"
    data = {
        "ajax": "CreateAward",
        "playerids": ",".join(ids),
        "reason": reason,
        "cost": amount,
        "location": common.server,
        "awardedby": common.bot_name
    }
    return send(pool, data)


# command: award item to a player
def award_item(player, item, amount, pool):
    if player not in common.player_info:
        return False, "The player does not exist"
    data = {
        "ajax": "CreateItemAward",
        "playerid": common.player_info[player]["id"],
        "item": item,
        "cost": amount,
        "location": common.server,
        "awardedby": common.bot_name,
        "zerosum": ""
    }
    return send(pool, data)


# command: add a player to all DKP tables
def addPlayer(player, player_class):
    print(common.clan)
    for pool in common.table_ids:
        data = {
            "ajax": "AddPlayer",
            "name": player,
            "playerguild": common.clan,
            "playerclass": player_class,
            "dkp": 0
        }
        send(pool, data)
    return


# command: log in from the bot
def login():
    data = {
        "siteUserEvent": "login",
        "username": common.username,
        "password": common.password
    }
    r = requests.post(url="https://webdkp.com/login", data=data)
    cookie = ""
    cookies = r.cookies.get_dict()
    for k in cookies:
        cookie += k + "=" + cookies[k] + ";"
    common.headers = {"Cookie": cookie}
