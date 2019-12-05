import json, requests
from TOK import TokenGiphy
API_KEY=TokenGiphy
#api.giphy.com/v1/gifs/random



class Giphy:
    def __init(self):
        pass
    def randomGif(self,tag):
        r = requests.get(url =f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={tag}&rating=R")
        print(f"request for a gif response : {r}")

        #print(r.text)
        rtxt = json.loads(r.text)
        if rtxt["data"] != [] :
            #print(r.text)
            rtxt = json.loads(r.text)
            #print(rtxt)
            return(f"{rtxt['data']['url']} POWERED By Giphy")
        else :
            return("nombre de requêtes limitées par l'api")

if __name__ == "__main__":
    g = Giphy
    g.randomGif("trump")
