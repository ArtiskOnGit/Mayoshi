import json, requests
API_KEY="S8fuxlIkUP9iSv3GKfG6NhXYlwDRYpVs"
#api.giphy.com/v1/gifs/random



class Giphy:
    def __init(self):
        pass
    def randomGif(self,tag):
        r = requests.get(url =f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={tag}&rating=R")
        print(r)

        #print(r.text)
        rtxt = json.loads(r.text)
        if rtxt["data"] != [] :
            print(r.text)
            rtxt = json.loads(r.text)
            print(rtxt)
            return(f"{rtxt['data']['url']} - Powered by Giphy")
        else :
            return("You are being rate-limited by Giphy API")

if __name__ == "__main__":
    g = Giphy
    g.randomGif("trump")
