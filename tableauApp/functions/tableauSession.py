import tableauserverclient as TSC
import getpass
import configparser
import os
import sys

class TableauSession():

    def __init__(self, serverUrl, username, password, site):
        self.serverUrl = serverUrl
        self.username = username
        self.password = password
        self.site = site

    def connectToServer(self):
        try:
            self.tableau_auth = TSC.TableauAuth(self.username, self.password, self.site)
            self.serverConnection = TSC.Server(self.serverUrl, use_server_version=True)
            self.serverConnection.auth.sign_in(self.tableau_auth)
            print("\n----------------------------------------------------------\n")
            print("Connected to the Tableau Server!")
            s_info = self.serverConnection.server_info.get()
            print("\nServer info:")
            print("\tProduct version: {0}".format(s_info.product_version))
            print("\tREST API version: {0}".format(s_info.rest_api_version))
            print("\tBuild number: {0}".format(s_info.build_number))
            print("\tAddress: {}".format(self.serverConnection.server_address))
            print("\tUsername: {}".format(self.username))
            print("\tSite name: {}".format(self.site))
            print("\n----------------------------------------------------------\n")
            return 1
        except: 
            print("\nInvalid login information!!!")
            print("Error: {}".format(sys.exc_info()))
            return ""
    
    def disconnectFromServer(self):
        self.serverConnection.auth.sign_out()
        print("Disconnecting from Tableau Server")
    
    def listSites(self):
        self.sites=self.serverConnection.sites.get()[0]
        for i,s in enumerate(self.sites):
            print("{}: {}\n\tURL: {}\n\tUser quota: {}\n\tStorage quota: {}\n\tState: {}\n".format(i,s.name,s.content_url,s.user_quota,s.storage_quota,s.state))
    
    def listProjects(self):
        self.projects=self.serverConnection.projects.get()[0]
        for i,p in enumerate(self.projects):
            print("{}: {}\n\tDescription: {}\n\tId: {}\n\tParent id: {}\n\tPermissions: {}\n".format(i,p.name,p.description,p.id,p.parent_id,p.content_permissions))
    
    def listWorkbooks(self):
        self.workbooks = self.serverConnection.workbooks.get()[0]
        self.workbooks = [(w,w.project_name) for w in self.workbooks]
        self.workbooks.sort(key=lambda tup: tup[1])
        listOfProjects = list(set([w[1] for w in self.workbooks]))
        for p in listOfProjects: 
            counter=0
            print("\nProject name: {}".format(p))
            print("")
            for w in self.workbooks:
                if w[1]==p:
                    counter+=1
                    self.serverConnection.workbooks.populate_connections(w[0])
                    connections=[connection.datasource_name for connection in w[0].connections]
                    print("\t-{}) {} \n\t\tOwner: {} \n\t\tConnections: {}".format(counter,w[0].name,w[0].owner_id,connections))
    
    def listDataSources(self):
        self.dataSources = self.serverConnection.datasources.get()[0]
        for i,d in enumerate(self.dataSources):
            print("{}: {}\n\tId: {}\n\tProject name: {}\n\tType: {}\n\tUpdated at:".format(i,d.name,d.id,d.project_name,d.datasource_type,d.updated_at))
        return ""