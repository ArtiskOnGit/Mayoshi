import wikipedia

class wiki:
    def WSearch(input):
        try :
            s = wikipedia.page(str(input))
            print (f"Wiki search for {s.title}")
            return(wikipedia.summary(input,sentences = 2))
        except wikipedia.exceptions.DisambiguationError as e: #Handling of disambiguation error from wikipedia api
            e = str(e)
            e = e.replace("\n",", ")

            return(f"Disambiguation Error, search for something more precise. : {e}")

if __name__ == "__main__":
    print("\n" + wiki.WSearch("Mu"))
