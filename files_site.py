import os
import magic
from flask import *
import json

user = os.getlogin()
ur = f'/media/{user}/EEB3-5227'

os.chdir(ur)
app = Flask(__name__, template_folder=f'/home/{user}/files_site/static')


def get_files(path_to_folder):
    os.chdir(path_to_folder)
    files = os.listdir()
    files1 = []
    for file in files:
        path = f'{path_to_folder}/{file}'
        js = {
            'is_dir': os.path.isdir(path),
            'name': file,
            'b': get_b(path),
            'type': get_type(path)
        }
        files1.append(js)
    return jsonify(files1)


def get_size_file_in_direct(path):
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size


def get_b(path):
    if os.path.isdir(path):
        return get_size_file_in_direct(path)
    else:
        return os.path.getsize(path)


def get_type(path):
    if os.path.isdir(path):
        return 'folder'
    else:
        return magic.from_file(path)


@app.route('/files')
def my_files():
    return render_template('files_site.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete_f():
    path = request.get_data(as_text=True)
    path = json.loads(path)
    path = path['path'] + '/' + path['name']
    mas2 = path.split('/')
    while mas2.count('') > 0:
        mas2.remove('')
    mas = []
    z = 0
    for p in mas2:
        if z < len(mas2) - 1:
            mas.append(p)
        z += 1
    path1 = f'/{"/".join(mas)}'
    os.chdir(ur + path1)
    if os.path.isdir(ur + path):
        os.rmdir(ur + path)
    else:
        os.remove(ur + path)
    return get_files(ur + path)


@app.route('/rename', methods=['POST', 'GET'])
def rename_f():
    data = request.get_data(as_text=True)
    js = json.loads(data)
    path = ur + '/' + js['path']
    try:
        os.chdir(path)
        os.rename(js['name'], js['new_name'].replace(' ', '_'))
        return get_files(path)
    except:
        return 'Error'


@app.route('/cr_f', methods=['POST', 'GET'])
def ch_f():
    data = request.get_data(as_text=True)
    js = json.loads(data)
    os.chdir(ur + '/' + js['path'])
    os.mkdir(js['name'])
    return get_files(ur + '/' + js['path'])


@app.route('/get_my_files', methods=['POST', 'GET'])
def get_my_files():
    data = request.get_data(as_text=True)
    js = json.loads(data)
    os.chdir(f"{ur}{js['path']}")
    return get_files(f"{ur}{js['path']}")


@app.route('/download', methods=['POST', 'GET'])
def download():
    data = request.get_data(as_text=True)
    js = json.loads(data)
    return send_from_directory(ur + js['path'], js['name'])


if __name__ == '__main__':
    app.run(host='192.168.8.105')
