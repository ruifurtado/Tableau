from functions.tableauSession import TableauSession
import os
import getpass
import configparser
import argparse

configPath='../myconfig.ini'

def initSession():
    serverUrl=""
    username=""
    password=""
    site=""
    if os.path.isfile(configPath):
        answer=input("\nConfiguration file available. Do you want to use it (Yes/No)?: ")
        if answer=='Yes':
            config = configparser.ConfigParser()
            config.read(configPath)
            serverUrl = config['SESSION']['server']
            username = config['SESSION']['username']
            password = config['SESSION']['password']
            site = config['SESSION']['site']
        if answer=='No':
            print("\n-> Input user parameters\n")
            serverUrl = input("Server link: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            site = input("Site: ")
    session=TableauSession(serverUrl,username,password,site)
    return session

def actionToTake(argument,session):
    switcher = {
        1:listSites(session),
        2:listProjects(session),
        3:listWorkbooks(session),
        4:listDataSources(session),
        5:exit(session)
    }
    func=switcher.get(int(argument),lambda:'Invalid input')  # Get the function from switcher dictionary
    return func

def listSites(session):
    session.listSites()
    return ""

def listProjects(session):
    session.listProjects()
    return ""

def listWorkbooks(session):
    session.listWorkbooks()
    return ""
def listDataSources(session):
    session.listDataSources()
    return ""

def exit(session):
    session.disconnectFromServer()
    return 'exit'

def main():
    print("\n------------------WELCOME TO TABLEAU APP------------------")
    connection=""
    while connection=="":
        session=initSession()
        connection=session.connectToServer()
    while True:
        print("1: List sites\n2: List projects\n3: List workbooks\n4: List data sources\n5: Exit\n")
        action = input("Action to take: ") 
        print("")
        result=actionToTake(action,session)
        if result=="exit":
            break

if __name__ == "__main__":
    main()    