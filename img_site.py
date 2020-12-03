from flask import *
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='/home/voven4ek/PycharmProjects/voven4ek_web/')
dasks = []
socket = SocketIO(app)


@app.route('/draw')
def home():
    return render_template('img_site.html')


@app.route('/look')
def send_png():
    return render_template('look.html')


@socket.on('send')
def send(data):
    emit("get"+data['id_t'], {'png': str(data['png']), 'name': data['name']}, broadcast=True)


@socket.on('help')
def send(data):
    emit("help"+data['id_t'], {}, broadcast=True)


@socket.on('answer')
def send(data):
    emit("help"+data['id_t'], {}, broadcast=True)


@socket.on("chat")
def chat(data):
    data['message'] = f'''
    <div style='background-color: #38C9A3; padding: 15px; border-radius: 10px; color: white;'>
    <h3 style='background-color: green; padding: 15px; border-radius: 10px; color: white;'>
    {data['name']} writing:
    </h3>
    <h4>
    {data['message']}
    </h4>
    </div>
    <br>
    <br>
    <br>
    '''
    emit("message"+data['id_t'], {'message': data['message']}, broadcast=True)


if __name__ == '__main__':
    app.run(host='192.168.1.103')
