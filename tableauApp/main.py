from functions.tableauSession import TableauSession
import os
import getpass
import configparser
import argparse

def initializeSession():
    session=TableauSession()
    while session.connected==0:
        session=session.initSession()
        session=session.connectToServer()
    return session

def actionToTake(argument,session):
    func=""
    if int(argument)==1:
        func=listSites(session)
    elif int(argument)==2:
        func=listProjects(session)
    elif int(argument)==3:
        func=listWorkbooks(session)
    elif int(argument)==4:
        func=listDataSources(session)
    elif int(argument)==5:
        func=exit(session)
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
    session = initializeSession()
    result=""
    while result!="exit":
        action = 0
        result = 0
        print("1: List sites\n2: List projects\n3: List workbooks\n4: List data sources\n5: Exit\n")
        action = input("Action to take: ") 
        result=actionToTake(action,session)

if __name__ == "__main__":
    main()    