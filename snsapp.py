# For using this python, you fist need to install aws cli and aws configure
# Then you need to modify groupname
# Also you can modify alarm put_metric_alarm according to your need
# If you want to create resource group for CloudFront, the region must be us-east-1

from flask import Flask
from flask_socketio import SocketIO, emit
import json
import gsm0338

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins = '*')


@app.route('/')

def app_run(msg):
    mess = str(msg['message'])

    try:
        messa = u'{' + mess + '}'
        encode = messa.encode('gsm03.38')
        length = len(mess)
        if length < 161:
            response = "此短信可以被gsm03.38编码且长度等于" + str(length) + "个字符小于161个字符的拆分限制"
        else:
            response = "此短信可以被gsm03.38编码且长度等于" + str(length) + "个字符需要被拆分"
        return response
    except:
        length = len(mess)
        if length < 71:
            response = "此短信不能被gsm03.38编码且长度等于" + str(length) + "个字符小于71个字符的拆分限制"
        else:
            response = "此短信不能被gsm03.38编码且长度等于" + str(length) + "个字符需要被拆分"
        return response


@socketio.on('connect')
def socketio_connect():
    print('Client has connected to the backend')
    emit('event', {'message': 'ACK'})


@socketio.on('process')
def socketio_message_event(message):
    print('Received event: ' + str(message))
    response = app_run(json.loads(message))
    emit('response', {'message': response})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=5000)
