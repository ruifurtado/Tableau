import tableauserverclient as TSC
import getpass
import configparser
import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import zipfile

# TODO Create more atribute inherited from the tableau session and also other like the actual workbook object that should be 
# inside the object stored

class TableauWorkbook():

    def __init__(self, session):
        self.session=session
        self.name=""
    
    def initWorkbook(self):
        if os.path.isfile('../myconfig.ini'): # [RESOURCES] must be on the file, create something that enables this check
            answer=input("Configuration file available. Do you want to use it (Yes/No)?: ")
            if answer=='Yes':
                config = configparser.ConfigParser()
                config.read('../myconfig.ini')
                self.name = config['WORKBOOK']['workbookName']
                if config['WORKBOOK']['downloadPath']!="" or config['WORKBOOK']['downloadPath']!=self.downloadPath:
                    self.repositoryPath=config['WORKBOOK']['downloadPath']
            if answer=='No':
                self.name = input("Name of the workbook to be updated/downloaded: ")
    
    
    def download(self):
        workbooks = self.session.serverConnection.workbooks.get()
        targetWorkbook = [w for w in workbooks[0] if w.name==self.name]
        self.id=targetWorkbook[0].id
        self.session.serverConnection.workbooks.download(self.id, filepath=self.repositoryPath, no_extract=False)
        print("Workbook downloaded!")
        self.session.serverConnection.workbooks.populate_connections(targetWorkbook[0])
        connections=[connection.datasource_name for connection in targetWorkbook[0].connections]
        print("\n\t-{} \n\t\tOwner: {} \n\t\tConnections: {}\n".format(targetWorkbook[0].name,targetWorkbook[0].owner_id,connections))     
        return ""

    def update(self): # Make diferent update options available: update workbook only, update workbooks+ds ...
        #filename='C:/Users/efrtrxx/Ericsson AB/S&R ds - Documents/tableau_requests/knowledge_mgmt_metis_tableau/MELA_Metis_June_2019_Data.xlsx'
        filename="C:/Users/efrtrxx/Ericsson AB/S&R ds - Documents/tableau_requests/tableau_apis/tableauApp/repository/MELA_Metis_June_2019_Data.xls"
        workbookPath='..\\repository\\Test Workbook.twbx'
        if os.path.isfile(workbookPath):
            if '.twbx' in workbookPath:
                print("\nFile provided is not a twb! It is going to be decoded")
                with zipfile.ZipFile(workbookPath, 'r') as zip_ref:
                    zip_ref.extractall(self.repositoryPath)
            workbookPath=workbookPath[:-1].replace(" ","")
            print("\nWorkbook saved as twb. Path: {}\n".format(workbookPath))
        tree = ET.parse(workbookPath)
        root = tree.getroot()
        for element in root.iter('connection'):
            if 'filename' in element.attrib.keys():
                element.attrib['filename']=filename
                element.set('updated','yes')
        tree.write(workbookPath)
        print("\nWorkbook updated !")
        publish()

    def publish(self):
        wb_item = TSC.WorkbookItem(name=self.name, project_id=self.id)
        wb_item = self.session.workbooks.publish(wb_item, '..\\repository\\Test Workbook.twb', 'Overwrite')


   

