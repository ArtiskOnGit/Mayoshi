import wikipedia

class wiki:
    def WSearch(input):
        s = wikipedia.page(str(input))
        print (f"Wiki search for {s.title}")
        return(wikipedia.summary(input,sentences = 2))

if __name__ == "__main__":
    wiki.WSearch("Barack")
