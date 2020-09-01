import csv
import sys
import configparser
import requests


config = configparser.ConfigParser()
config.read('okta-config.txt')
url = config.get('General', 'url')
token = config.get('General', 'token')
fileName = config.get('General', 'filename')

def createStagedUser (firstName, lastName, email, login):
    jsonTosend = {"profile": {"firstName": firstName, "lastName": lastName, "email": email, "login": login}}
    res = requests.post(url+'/api/v1/users?activate', headers={'Accept': 'application/json', 'Content-Type':'application/json', 'Authorization': 'SSWS '+token}, json=jsonTosend)
    if res.status_code == 200:
        print('user created')
    else:
        print('user not created')
    return res.status_code

def updateUser (firstName, lastName, email, login,value):
    res = requests.get(url + '/api/v1/users/' + login,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token})
    # print('response from server:', res.text)
    dictFromServer = res.json()
    id = dictFromServer['id']
    #print(id)
    if res.status_code == 200:
        jsonTosend = {"profile": {"title": value}}
        #print(jsonTosend)
        res = requests.post(url+'/api/v1/users/' +id, headers={'Accept': 'application/json', 'Content-Type':'application/json', 'Authorization': 'SSWS '+token}, json=jsonTosend)
        print('user updated')
    else:
        print('User updation Failed')
    return res.status_code

def assignApp (firstName, lastName, email, login,Appname):
    res = requests.get(url + '/api/v1/users/' + login,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token})
    # print('response from server:', res.text)
    dictFromServer = res.json()
    id = dictFromServer['id']
    #print(id)
    res1= res = requests.get(url+'/api/v1/apps?q='+Appname,headers={'Accept':'application/json','Content-Type':'application/json', 'Authorization': 'SSWS '+token})
    dictFromServer = res1.json()
    appid = dictFromServer[0]['id']
    #print(appid)
    if res1.status_code == 200:
        result = requests.put(url+'/api/v1/apps/'+appid+'/users/'+id,headers={'Accept':'application/json','Content-Type':'application/json', 'Authorization': 'SSWS '+token})
        print('user assigned to app')
    else:
        print('User assignment Failed')
    return result.status_code

def deactivateUser (firstName, lastName, email, login):
    res = requests.get(url + '/api/v1/users/' + login,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token})
    # print('response from server:', res.text)
    dictFromServer = res.json()
    userid = dictFromServer['id']
    if res.status_code == 200:
        result = requests.post(url + '/api/v1/users/' + userid + '/lifecycle/deactivate',headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token})
        result1 = requests.delete(url + '/api/v1/users/' + userid,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token})
        print('user deleted')
    else:
        print('User Deletion Failed')
    return res.status_code

with open(fileName,'r') as File:
    reader = csv.reader(File, delimiter=',')
    next(reader)
    for row in reader:
        try:
            operation = row[6]
        except IndexError:
            operation = 'null'

        if operation == 'Create':
            createStagedUser(row[0],row[1],row[2],row[3])

        elif operation == 'Delete':
           deactivateUser(row[0],row[1],row[2],row[3])

        elif operation == 'Assignapp':
           assignApp(row[0],row[1],row[2],row[3],row[5])

        elif operation == 'Update':
           updateUser(row[0],row[1],row[2],row[3],row[4])

        else:
           print('No operation defined')

