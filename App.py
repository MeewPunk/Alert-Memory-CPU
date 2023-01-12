from flask import Flask, render_template,redirect, url_for, request
import threading
import webbrowser,json,random
from binance.client import Client
from os import path
from colorama import Style
from clint.textui import colored
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
import os,requests
import shutil,psutil
import os, signal


app = Flask(__name__, static_url_path=r'/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
Msg = ''
history = ''

def Check_Usage(CPU,RAM):

    Data = []
    with open(r'AppsData\data.json',encoding='utf8') as fp:
        Data = json.load(fp)

    Config = []
    with open(r'AppsData\Token.json',encoding='utf8') as fp:
        Config = json.load(fp)

    # CPU_Usage
    
    if  float(CPU) >= float(Data[0]['Let_CPU']) and Data[0]['CPU_Notify'] == 'True':

        # connect  line ----------------------------------------------------
        Line_token = Config[0]['Token']
        url_line = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+Line_token}
        
        # connect  line ----------------------------------------------------
        Message = Data[0]['Msg_CPU']
        requests.post(url_line, headers=headers, data = {'message':Message}) 

        lists = []
        lists.append({
            "Let_CPU" : Data[0]['Let_CPU'],
            "Msg_CPU" : Data[0]['Msg_CPU'],
            "CPU_Notify" : 'False',
            "Let_RAM" : Data[0]['Let_RAM'],
            "Msg_RAM" : Data[0]['Msg_RAM'],
            "RAM_Notify" : Data[0]['RAM_Notify']
            })


        with open(r'AppsData\data.json', 'w', encoding='utf8') as json_file:
            json.dump(lists, json_file, indent=4,ensure_ascii=False)

    # RAM_Usage
    if  float(RAM) >= float(Data[0]['Let_RAM']) and Data[0]['RAM_Notify'] == 'True' :
        # connect  line ----------------------------------------------------
        Line_token = Config[0]['Token']
        url_line = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+Line_token}
        
        # connect  line ----------------------------------------------------
        Message = Data[0]['Msg_RAM']
        requests.post(url_line, headers=headers, data = {'message':Message}) 
        
        lists = []
        lists.append({
            "Let_CPU" : Data[0]['Let_CPU'],
            "Msg_CPU" : Data[0]['Msg_CPU'],
            "CPU_Notify" : Data[0]['CPU_Notify'],
            "Let_RAM" : Data[0]['Let_RAM'],
            "Msg_RAM" : Data[0]['Msg_RAM'],
            "RAM_Notify" : 'False'
            })


        with open(r'AppsData\data.json', 'w', encoding='utf8') as json_file:
            json.dump(lists, json_file, indent=4,ensure_ascii=False)

@app.route('/') 
def Dashboard():

    Config = []
    with open(r'AppsData\Token.json',encoding='utf8') as fp:
        Config = json.load(fp)

    Data = []
    with open(r'AppsData\data.json',encoding='utf8') as fp:
        Data = json.load(fp)

    total, used, free = shutil.disk_usage("/")
    mem_usage = psutil.virtual_memory()

    data = {
        'Token': Config[0]['Token'],
        'Let_CPU': Data[0]['Let_CPU'],
        'Msg_CPU': Data[0]['Msg_CPU'],
        'Let_RAM': Data[0]['Let_RAM'],
        'Msg_RAM': Data[0]['Msg_RAM'],
        'CPU_Usage' : str(psutil.cpu_percent(4)),
        'RAM_Usage' : str(mem_usage.percent),
        'Disk_Free' : str(free // (2**30)),
        'Msg': Msg
        
    }
    return render_template('index.html', data = data)

@app.route('/Logout')
def Logout():
    os.kill(os.getpid(), signal.SIGINT)
    return "200"


@app.route('/Token',methods = ['POST'])
def Token():
    global Msg

    if request.method == 'POST':

        lists = []
        lists.append({"Token" : request.form['Token']})

        with open(r'AppsData\Token.json', 'w', encoding='utf8') as json_file:
            json.dump(lists, json_file, indent=4,ensure_ascii=False)

        Config = []
        with open(r'AppsData\Token.json',encoding='utf8') as fp:
            Config = json.load(fp)

        # connect  line ----------------------------------------------------
        Line_token = Config[0]['Token']
        url_line = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+Line_token}
        
        # connect  line ----------------------------------------------------
        Message = request.form['Mgs_Token']
        requests.post(url_line, headers=headers, data = {'message':Message}) 

        Msg = 'ส่งข้อความไปทางไลน์แล้ว'
        return redirect('/')


@app.route('/data',methods = ['POST'])
def Data():
    global Msg
    if request.method == 'POST':


        lists = []
        lists.append({
            "Let_CPU" : request.form['Let_CPU'],
            "Msg_CPU" : request.form['Msg_CPU'],
            "CPU_Notify" : 'True',
            "Let_RAM" : request.form['Let_RAM'],
            "Msg_RAM" : request.form['Msg_RAM'],
            "RAM_Notify" : 'True'
            })


        with open(r'AppsData\data.json', 'w', encoding='utf8') as json_file:
            json.dump(lists, json_file, indent=4,ensure_ascii=False)

        Msg = 'บันทึกรายการสำเร็จ'
        return redirect('/')

# socketio ----------------------------------------

@socketio.on('my event')
def handle_my_custom_event(json):

    total, used, free = shutil.disk_usage("/")
    mem_usage = psutil.virtual_memory()

    Check_Usage(psutil.cpu_percent(4),mem_usage.percent)

    data={
        'CPU_Usage' : str(psutil.cpu_percent(4)),
        'RAM_Usage' : str(mem_usage.percent),
        'Disk_Free' : str(free // (2**30))
    }

    emit('my response', data)


# socketio ----------------------------------------

port = 50501
url = "http://127.0.0.1:{0}".format(port)

threading.Timer(1.25, lambda: webbrowser.open(url) ).start()


if __name__ == '__main__':
    socketio.run(app,port=port)



    
