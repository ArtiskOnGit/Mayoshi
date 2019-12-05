import requests
import json




URLFORTNITE  = "https://api.fortnitetracker.com/v1/store"

#api_key = "13d2fcf6-915f-46c4-bc0a-6eac384b0892"

def get_value(listOfDicts, key):
    for subVal in listOfDicts:
        if subVal["key"] ==  key:
            return subVal["value"]

# r = requests.get(url = URLFORTNITE, headers = {"TRN-Api-Key" : "13d2fcf6-915f-46c4-bc0a-6eac384b0892"})
#
# print(r.text)
# f = open ("test.json",'w')
# f.write(json.dumps(r.text, indent = 4 ))
# f.close()


class stat:
    def __init__(self):
        pass


    def getPlayerId(self,player,plateform):
        r = requests.get(url = f"https://api.fortnitetracker.com/v1/profile/{plateform}/{player}/", headers = {"TRN-Api-Key" : "13d2fcf6-915f-46c4-bc0a-6eac384b0892"})
        txt = json.loads(r.text)
        return(txt["accountId"])


    def player(self,player,plateform,actual):
        print(f"https://api.fortnitetracker.com/v1/profile/{plateform}/{player}/")
        r = requests.get(url = f"https://api.fortnitetracker.com/v1/profile/{plateform}/{player}/", headers = {"TRN-Api-Key" : "13d2fcf6-915f-46c4-bc0a-6eac384b0892"})
        #print(r.text)
        print(r)

        if "It's not you, it's us. We had an error. These things happen. If it keeps happening, please" in r.text :
            return("It seems that you aren't in Fortnite Tracker, or that you misspelled your nickname. Try directly from their website : https://fortnitetracker.com/")
        elif "40" in r:
            return("Fortnite Trackers' servers aren't accessible. Try again later !")
        else:
            with open("test.html", "w", encoding = "utf-8") as f:
                f.write(r.text)

            txt = json.loads(r.text)

            #print(f"Nombre de top 1 : {txt['lifeTimeStats'][]['value']}")

            if actual :
                kills = txt['stats']['curr_p2']['kills']['valueInt'] + txt['stats']['curr_p10']['kills']['valueInt']+txt['stats']['curr_p9']['kills']['valueInt']
                matches = txt['stats']['curr_p2']['matches']['valueInt'] + txt['stats']['curr_p10']['matches']['valueInt']+txt['stats']['curr_p9']['matches']['valueInt']
                KD = round(kills/matches,2)
                wins = txt['stats']['curr_p2']['top1']['valueInt'] + txt['stats']['curr_p10']['top1']['valueInt']+txt['stats']['curr_p9']['top1']['valueInt']




                ret = f"""Pseudo : {player}
Number of Top #1 this season : {wins}
Number of kills this season : {kills}
K/D ratio this season : {KD}

Solo Top #1 this season : {txt['stats']['curr_p2']['top1']['value']}
Solo K/D ratio this season : {txt['stats']['curr_p2']['kd']['value']}

Duo Top #1 this season : {txt['stats']['curr_p10']['top1']['value']}
Duo K/D Ratio this season : {txt['stats']['curr_p10']['kd']['value']}

Nombre de top 1 en squad cette saison : {txt['stats']['curr_p9']['top1']['value']}
Kd en squad cette saison : {txt['stats']['curr_p9']['kd']['value']}"""
            else:

                ret = f"""Pseudo : {player}
Total Top #1 this season: {get_value(txt['lifeTimeStats'], 'Wins')}
Total kills this season : {get_value(txt['lifeTimeStats'], 'Kills')}
K/D Ratio : {get_value(txt['lifeTimeStats'], 'K/d')}

Solo Top #1 overall : {txt['stats']['p2']['top1']['value']}
Solo K/D Ratio overall : {txt['stats']['p2']['kd']['value']}

Duo Top #1 overall : {txt['stats']['p10']['top1']['value']}
Duo K/D Ratio overall: {txt['stats']['p10']['kd']['value']}

Squad Top #1 overall : {txt['stats']['p9']['top1']['value']}
Squad K/D Ratio overall : {txt['stats']['p9']['kd']['value']}"""
            print(ret)
            return(ret)

    def lastGame(self,player):
        r = requests.get(url = f"GET https://api.fortnitetracker.com/v1/profile/account/{self.getPlayerId(player,'pc')}/matches/", headers = {"TRN-Api-Key" : "13d2fcf6-915f-46c4-bc0a-6eac384b0892"})
        with open("historic.html", "w", encoding = "utf-8") as f:
            f.write(r.text)






#stat.player(input("Nickname >> "),input("Platform >> "),True)
