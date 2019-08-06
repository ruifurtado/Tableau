import argparse
import getpass
import logging
import tableauserverclient as TSC
import os 

def getParameters():
    if os.path.isfile('./myconfig.ini'):
        answer=input("Configutation file available. Do you want to use it (Yes/No)?: ")
        print(answer)
    else:
        parseInput()

def parseInput():
    parser = argparse.ArgumentParser(description='Get all of the refresh tasks available on a server')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('--site', '-S', default=None)
    parser.add_argument('--password', '-p', default='071428xit256Guy', help='if not specified, you will be prompted')

    parser.add_argument('--logging-level', '-l', choices=['debug', 'info', 'error'], default='error',
                        help='desired logging level (set to error by default)')

    parser.add_argument('resource_type', choices=['workbook', 'datasource'])
    parser.add_argument('resource_name')

    args = parser.parse_args()

    if args.password is None:
        password = getpass.getpass("Password: ")
    else:
        password = args.password

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    return args, password


def signIn(args,password):
     # SIGN IN
    tableau_auth = TSC.TableauAuth(args.username, password, args.site)
    #print('Im heeere')
    server = TSC.Server(args.server)
    req_option = TSC.RequestOptions()
    #print('Im r')
    with server.auth.sign_in(tableau_auth):
        #print('Im r')
        server.use_highest_version()
        if args.resource_type == "workbook":
            # Get the workbook by its Id to make sure it exists
            print(args.resource_name)
            req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,TSC.RequestOptions.Operator.Equals,args.resource_name))

            resource,pagination_item = server.workbooks.get(req_option)

            # trigger the refresh, you'll get a job id back which can be used to poll for when the refresh is done
            print("Resource name: {}".format(resource[0].name))
            print("Resource id: {}".format(resource[0].id))
            results = server.workbooks.download(resource[0].id)
            #print(resource[0][0].name)
        else:
            # Get the datasource by its Id to make sure it exists
            resource = server.datasources.get_by_id(args.resource_name)

            # trigger the refresh, you'll get a job id back which can be used to poll for when the refresh is done
            results = server.datasources.refresh(resource)

        #print(results)

def downloadFunc():
    getParameters()
    #args,password=parseInput()
    #signIn(args,password)
   
#if __name__ == '__main__':
#    main()