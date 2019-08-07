import getpass
import os
import configparser
import tableauserverclient as TSC
import argparse

serverObject=""

def exit():
    return "exit"

def help():
    return ""

def downloadResource(): # TODO HERE: make the function check if the file exists or not
    path = r'.\download'
    resourceType=""
    resourceName=""
    if os.path.isfile('./myconfig.ini'): # [RESOURCES] must be on the file, create something that enables this check
        answer=input("Configuration file available. Do you want to use it (Yes/No)?: ")
        if answer=='Yes':
            config = configparser.ConfigParser()
            config.read('myconfig.ini')
            resourceName = config['RESOURCES']['resource_name']
            resourceType = config['RESOURCES']['resource_type']
        if answer=='No':
            print("-> Input resource parameters\n")
            resourceName = input("Workbook name: ")
            resourceType = input("Resource type (workbook/datasource): ")
            pathAnswer = input("Do you want to specify a path for the downloaded resource (Yes/No)?: ") # put tkinter here!
            if pathAnswer=="Yes":
                path = input("Specify your path: ")
    if resourceType=="workbook":
        workbooks = serverObject.workbooks.get()
        targetWorkbook = [w for w in workbooks[0] if w.name==resourceName]
        serverObject.workbooks.download(targetWorkbook[0].id, filepath=path, no_extract=False)
        print("Workbook downloaded!")
        serverObject.workbooks.populate_connections(targetWorkbook[0])
        connections=[connection.datasource_name for connection in targetWorkbook[0].connections]
        print("\n\t-{} \n\t\tOwner: {} \n\t\tConnections: {}\n".format(targetWorkbook[0].name,targetWorkbook[0].owner_id,connections))     
    if resourceType=="datasource":
        datasources = serverObject.datasources.get()
        targetDatasource = [d for d in datasources[0] if d.name==resourceName]
        serverObject.datasources.download(targetDatasource[0].id, filepath=path, no_extract=False)
    return ""

def downloadDataSource():
    return ""

def listDataSources():
    return ""

def listProjects():
    projects = serverObject.projects.get()
    for i,p in enumerate(projects[0]):
        print("{}: {}\n\tDescription: {}\n\tId: {}\n\tParent id: {}\n\tPermissions: {}\n".format(i,p.name,p.description,p.id,p.parent_id,p.content_permissions))
    return ""

def listWorkbooks():
    workbooks = serverObject.workbooks.get()
    workbooks = [(w,w.project_name) for w in workbooks[0]]
    workbooks.sort(key=lambda tup: tup[1])
    listOfProjects = list(set([w[1] for w in workbooks]))
    for p in listOfProjects: 
        counter=0
        print("\nProject name: {}".format(p))
        print("")
        for w in workbooks:
            if w[1]==p:
                counter+=1
                serverObject.workbooks.populate_connections(w[0])
                connections=[connection.datasource_name for connection in w[0].connections]
                print("\t-{}) {} \n\t\tOwner: {} \n\t\tConnections: {}".format(counter,w[0].name,w[0].owner_id,connections))      
    return ""

def listSites():
    sites=serverObject.sites.get()
    for i,s in enumerate(sites[0]):
        print("{}: {}\n\tURL: {}\n\tUser quota: {}\n\tStorage quota: {}\n\tState: {}\n".format(i,s.name,s.content_url,s.user_quota,s.storage_quota,s.state))
    return ""

def publishWorkbook():
    return ""

def publishDataSource():
    project_id = "8676e446-180c-4a17-bcdf-7842a8fd49e5"
    new_datasource = TSC.DatasourceItem(project_id)
    
    return ""

def actionToTake(argument):
    switcher = {
        1:listDataSources,
        2:listWorkbooks,
        3:listProjects,
        4:listSites,
        5:downloadResource,
        6:exit,
    }
    # Get the function from switcher dictionary
    func=switcher.get(int(argument),lambda:'Invalid input')
    # Execute the function
    return func()

def connectToServer():
    servername, username, password, site=parseInput()
    try:
        tableau_auth = TSC.TableauAuth(username, password, site)
        server = TSC.Server(servername, use_server_version=True)
        server.auth.sign_in(tableau_auth)
        print("\n----------------------------------------------------------\n")
        print("Connected to the Tableau Server!")
        s_info = server.server_info.get()
        print("\nServer info:")
        print("\tProduct version: {0}".format(s_info.product_version))
        print("\tREST API version: {0}".format(s_info.rest_api_version))
        print("\tBuild number: {0}".format(s_info.build_number))
        print("\tAddress: {}".format(server.server_address))
        print("\tUsername: {}".format(username))
        print("\tSite name: {}".format(site))
        print("\n----------------------------------------------------------\n")
        return server
    except: 
        print("\nInvalid login information!!!")
        return ""
    
def parseInput():
    servername=""
    username=""
    password=""
    site=""
    if os.path.isfile('./myconfig.ini'):
        answer=input("\nConfigutation file available. Do you want to use it (Yes/No)?: ")
        if answer=='Yes':
            config = configparser.ConfigParser()
            config.read('myconfig.ini')
            servername = config['PARAMETERS']['server']
            username = config['PARAMETERS']['username']
            password = config['PARAMETERS']['password']
            site = config['PARAMETERS']['site']
        if answer=='No':
            print("-> Input user parameters\n")
            servername = input("Server link: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            site = input("Site: ")

    return servername, username, password, site

if __name__ == "__main__":
    print("\n------------------WELCOME TO TABLEAU APP------------------")
    while serverObject=="":
        serverObject=connectToServer()
    while True:
        print("1: List data sources\n2: List workbooks\n3: List projects\n4: List sites\n5: Download resource\n6: Exit\n")
        action = input("Action to take: ") 
        print("")
        result=actionToTake(action)
        if result=="exit":
            break