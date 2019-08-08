import tableauserverclient as TSC
import getpass
import configparser
import os
import sys

class TableauDataSource():

    def __init__(self, session):
        self.session=session
        self.name=""
    
    # def initWorkbook(self):
    #     if os.path.isfile('../myconfig.ini'): # [RESOURCES] must be on the file, create something that enables this check
    #         answer=input("Configuration file available. Do you want to use it (Yes/No)?: ")
    #         if answer=='Yes':
    #             config = configparser.ConfigParser()
    #             config.read('../myconfig.ini')
    #             self.name = config['WORKBOOK']['workbook_name']
    #             if config['WORKBOOK']['download_path']!="" or config['WORKBOOK']['download_path']!=self.downloadPath:
    #                 self.downloadPath=config['WORKBOOK']['download_path']
    #         if answer=='No':
    #             self.name = input("Name of the workbook to be modified/updated: ")
    
    
    # def download(self):
    #     workbooks = self.session.serverConnection.workbooks.get()
    #     targetWorkbook = [w for w in workbooks[0] if w.name==self.name]
    #     self.session.serverConnection.workbooks.download(targetWorkbook[0].id, filepath=self.downloadPath, no_extract=False)
    #     print("Workbook downloaded!")
    #     self.session.serverConnection.workbooks.populate_connections(targetWorkbook[0])
    #     connections=[connection.datasource_name for connection in targetWorkbook[0].connections]
    #     print("\n\t-{} \n\t\tOwner: {} \n\t\tConnections: {}\n".format(targetWorkbook[0].name,targetWorkbook[0].owner_id,connections))     
    #     return ""

