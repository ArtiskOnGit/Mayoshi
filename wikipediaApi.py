import wikipedia

class wiki:
    def WSearch(input):
        try :
            s = wikipedia.page(str(input))
            print (f"Wiki search for {s.title}")
            return(wikipedia.summary(input,sentences = 2))
        except DisambiguationError:
            return("Disambiguation Error, search for something more precise.")

if __name__ == "__main__":
    wiki.WSearch("Barack")
