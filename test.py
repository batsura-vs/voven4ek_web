from random import randrange

from flask import *

app = Flask(__name__, template_folder="/home/voven4ek/PycharmProjects/voven4ek_web")
app.secret_key = hex(randrange(100, 1000))
site = 'http://192.168.1.84:5000/'
all_films = 4
options = [['Собачья жизнь', 'Бетховен', 'Маска', 'Путь домой', 'Белый плен'],
           ['Бриллиантовая рука', 'Джентельмены удачи', 'Приключения электроника', 'Джентельмены'],
           ['Один дома', 'Дети генирала', 'Сын полка', 'Могила Светлячков', 'Иваново детство'],
           ['Титаник', 'Настоящее преступление', 'Поймай меня если сможешь', 'Зелёная миля', 'Последняя миля'],
           ['1', '1', '1', '1', '1']]
films = ['1', '2', '3', '4', '']
answers = ['Маска', 'Бриллиантовая рука', 'Мальчик в полосатой пижаме', 'Зелёная миля', '']


@app.route('/')
def redactor():
    return render_template('menu.html', all=all_films)


@app.route('/test/<id_test>', methods=['post', 'get'])
def f(id_test):
    vidio = films[int(id_test) - 1]
    option = options[int(id_test) - 1]
    z = '#option selected@Ответ#opyion@'
    for a in option:
        z += '#option@'+a+'#/option@'
    return render_template('test_1.html', ready=id_test, ch=id_test, site=site, number=vidio, options=z,
                           test=all_films)


@app.route('/test/check/<id_test>', methods=['post', 'get'])
def f1(id_test):
    ans = request.form.get('answer')
    if 'test' + id_test in session:
        return render_template('Error.html')
    else:
        session['test' + id_test] = ans
        if str(ans).lower() == str(answers[int(id_test) - 1]).lower():
            a = 'corect.html'
            return render_template(a, col=id_test, fil=all_films, site=site)
        else:
            a = 'uncorect.html'
        return render_template(a, col=id_test, ans=answers[int(id_test) - 1], fil=all_films, site=site)


@app.route('/go')
def f3():
    z = 0
    for a in range(1, all_films + 1):
        if 'test' + str(a) in session:
            if str(session['test' + str(a)]).lower() == str(answers[a - 1]).lower():
                z += 1
    session.clear()
    return render_template('go.html', col=z, all=all_films)


if __name__ == '__main__':
    app.run(host='192.168.8.103', port='4999')
