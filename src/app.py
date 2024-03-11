from flask import Flask,render_template,redirect,request,session
from web3 import Web3,HTTPProvider
import json
import urllib3

def readData():
    req='https://api.thingspeak.com/channels/2456469/feeds.json'
    http=urllib3.PoolManager()
    response=http.request('get',req)
    # print(response.data)
    data=response.data.decode('utf-8')
    data=json.loads(data)
    data=data['feeds']
    return(data)

def readData1():
    req='https://api.thingspeak.com/channels/2456475/feeds.json'
    http=urllib3.PoolManager()
    response=http.request('get',req)
    # print(response.data)
    data=response.data.decode('utf-8')
    data=json.loads(data)
    data=data['feeds']
    return(data)

def readData2():
    req='https://api.thingspeak.com/channels/2456478/feeds.json'
    http=urllib3.PoolManager()
    response=http.request('get',req)
    # print(response.data)
    data=response.data.decode('utf-8')
    data=json.loads(data)
    data=data['feeds']
    return(data)

def readData3():
    req='https://api.thingspeak.com/channels/2456482/feeds.json'
    http=urllib3.PoolManager()
    response=http.request('get',req)
    # print(response.data)
    data=response.data.decode('utf-8')
    data=json.loads(data)
    data=data['feeds']
    return(data)

def preprocessData(data):
    cleandata=[]
    for i in data:
        dummy=[]
        dummy.append(i['created_at'])
        dummy.append(i['entry_id'])
        dummy.append(float(i['field1']))
        cleandata.append(dummy)
    return cleandata


app=Flask(__name__)
app.secret_key='1234'

def connect_with_RSU(acc):
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    if acc==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=acc

    artifact_path="./build/contracts/RSU.json"

    with open(artifact_path) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']

    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return contract,web3 

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/indexdata',methods=['post','get'])
def indexdata():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    if True:
        contract,web3=connect_with_RSU(0)
        tx_hash=contract.functions.addUser(username,password).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('index.html',res='user added')
    # except:
        # return render_template('index.html',res="user already added")

@app.route('/logindata',methods=['get','post'])
def logindata():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)
    contract,web3=connect_with_RSU(0)
    _usernames,_passwords=contract.functions.viewUsers().call()
    if username not in _usernames:
        return render_template('login.html',err='you dont have any account')
    for i in range(len(_usernames)):
        if(_usernames[i]==username and _passwords[i]==password):
            session['username']=username
            return redirect('/dashboard')
    return render_template('login.html',err='login invalid')

@app.route('/dashboard')
def dashboardPage():
    return render_template('dashboard.html')

@app.route('/model')
def modelPage():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        dummy=[]
        dummy.append(i[0])
        dummy.append(i[1])
        dummy.append(i[2])
        dummy.append('Traffic Blockage')
        mAlerts.append(dummy)
        
    return render_template('alerts.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model1')
def model1Page():
    data=readData1()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        dummy=[]
        dummy.append(i[0])
        dummy.append(i[1])
        dummy.append(i[2])
        dummy.append('Road Working on Progress')
        mAlerts.append(dummy)

    return render_template('alerts1.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model2')
def model2Page():
    data=readData2()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        dummy=[]
        dummy.append(i[0])
        dummy.append(i[1])
        dummy.append(i[2])
        dummy.append('Accident happened')
        mAlerts.append(dummy)

    return render_template('alerts2.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model3')
def model3Page():
    data=readData3()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        dummy=[]
        dummy.append(i[0])
        dummy.append(i[1])
        dummy.append(i[2])
        dummy.append('Road is Blocked')
        mAlerts.append(dummy)
        
    return render_template('alerts3.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=9001,debug=True)