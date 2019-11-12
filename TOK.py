from os import environ
Token = environ["TOKEN"]

if __name__ =="__main__":
    print(environ)
    print(environ["TOKEN"])
