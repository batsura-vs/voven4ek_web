from flask import *

app = Flask(__name__, template_folder="/home/voven4ek/IdeaProjects/voven4ek_web")


@app.route('/')
def redactor():
    return render_template('easy_m.html')


if __name__ == '__main__':
    app.run(host='192.168.8.103')