var PATH = [];
var one = (window.innerWidth + window.innerHeight) / 100;
var s = document.getElementById('back');
s.style.width = one * 3 + 'px';
s.style.height = one * 3 + 'px';
var s2 = document.getElementById('new_fol');
s2.style.width = one * 3 + 'px';
s2.style.height = one * 3 + 'px';

function carry(callback, arglist) {
    var thisObj = this;
    return (function () {
        callback.apply(thisObj, arglist)
    });
}

function socr_n(name, max) {
    if (name.indexOf('.') > 0 && name.length > max) {
        name = name.split('.')[0];
        var n = name.split('', max - 3);
        return n.join('') + '...';
    } else {
        var a = name.split('', max);
        return a.join('');
    }
}

function formatSizeUnits(bytes) {
    if (bytes >= 1073741824) {
        bytes = (bytes / 1073741824).toFixed(2) + ' GB';
    } else if (bytes >= 1048576) {
        bytes = (bytes / 1048576).toFixed(2) + ' MB';
    } else if (bytes >= 1024) {
        bytes = (bytes / 1024).toFixed(2) + ' KB';
    } else if (bytes > 1) {
        bytes = bytes + ' bytes';
    } else if (bytes === 1) {
        bytes = bytes + ' byte';
    } else {
        bytes = '0 byte';
    }
    return bytes;
}

function download_f(path, name) {
    var a = document.location.protocol;
    var b = document.location.host;
    var json = {
        path: path,
        name: name
    }
    fetch(a + '//' + b + '/download',
        {
            method: 'post',
            body: JSON.stringify(json)
        })
    alert('downloading!')
}

function ch_a(f, file) {
    var one = (window.innerWidth + window.innerHeight) / 100;
    if (f.is_dir) {
        var text = document.createElement('a');
        text.innerText = ': ' + socr_n(f.name, 15);
        text.style.display = 'inline-block';
        text.title = f.name;
        text.href = '#';
        text.style.fontSize = one + 'px';
        text.onclick = carry(click, [f.name]);
        file.appendChild(text);
    } else {
        var text1 = document.createElement('p');
        text1.innerText = ': ' + socr_n(f.name, 23);
        text1.style.display = 'inline-block';
        text1.title = f.name;
        text1.style.fontSize = one + 'px';
        file.appendChild(text1);
        var download = document.createElement('img');
        download.src = '/static/images/download.png';
        download.className = 'button';
        download.width = one * 3;
        download.height = one * 3;
        download.title = 'download file';
        download.align = "top";
        download.style.float = 'right';
        download.style.paddingRight = one + 'px';
        download.onclick = carry(download_f, [get_path() + '/' + f.name, f.name])
        file.appendChild(download);
    }
}


function back() {
    document.getElementById('files').innerHTML = '';
    PATH.pop();
    var json = {
        path: get_path()
    }
    send_to_server(json, '/get_my_files');
    document.getElementById('path').innerText = get_path();
}

function get_path() {
    if (PATH.length > 0) {
        return '/' + PATH.join('/');
    } else {
        return PATH.join('/');
    }
}

function del_f(file) {
    var su = confirm('Are you sure want to remove "' + file + '"?');
    if (su) {
        document.getElementById('files').innerHTML = '';
        var json = {
            path: get_path(),
            name: file
        }
        send_to_server(json, '/delete');
    } else {
    }
}

function cr_f() {
    var su = prompt('What will you name your file?');
    if (su !== null && su.length > 0) {
        document.getElementById('files').innerHTML = '';
        var json = {
            name: su,
            path: get_path()
        }
        send_to_server(json, '/cr_f');
    } else {
    }
}

function rename_f(file) {
    var name = '';
    var g = 0;
    while (name == null || 0 === name.length) {
        if (name == null) {
            g = 1;
            break
        } else {
            name = prompt('What will you name your file?');
        }
    }
    if (g === 0) {
        var h = '';
        for (var i = 0; PATH.length > i; i++) {
            h += PATH[i];
            if (i === 1) {

            } else if (PATH.length === i) {

            } else {
                h += '/';
            }
        }
        document.getElementById('files').innerHTML = '';
        var json = {
            name: file,
            new_name: name,
            path: get_path()
        }
        send_to_server(json, '/rename');
    }
}

function ref(files, a, b) {
    var one = (window.innerWidth + window.innerHeight) / 100;
    for (var i = 0; files.length > i; i++) {
        var file1 = files[i];
        var div = document.getElementById('files');
        var file = document.createElement('div');
        var icon = document.createElement('img');
        if (file1.is_dir) {
            icon.src = a + '//' + b + '/static/images/folder2.png';
            icon.title = 'it is folder';
        } else {
            icon.src = a + '//' + b + '/static/images/file.png';
            icon.title = 'it is file';
        }
        icon.width = one * 3;
        icon.align = "top";
        icon.height = one * 3;
        file.appendChild(icon);
        var text2 = document.createElement('p');
        if (file1.is_dir) {
            text2.innerText = 'Folder';
        } else {
            text2.innerText = 'File';
        }
        text2.style.display = 'inline-block';
        text2.style.paddingLeft = one + 'px';
        text2.style.fontSize = one + 'px';
        file.appendChild(text2);
        var rename = document.createElement('img');
        rename.src = '/static/images/rename.png';
        rename.className = 'button';
        rename.width = one * 3;
        rename.height = one * 3;
        rename.title = 'rename file';
        rename.align = "top";
        rename.style.float = 'right';
        rename.onclick = carry(rename_f, [file1.name]);
        file.appendChild(rename);
        var delete_f = document.createElement('img');
        delete_f.src = '/static/images/delete.png';
        delete_f.className = 'button';
        delete_f.width = one * 3;
        delete_f.height = one * 3;
        delete_f.align = "top";
        delete_f.title = 'delete file';
        delete_f.style.float = 'right';
        delete_f.style.paddingRight = one + 'px';
        delete_f.onclick = carry(del_f, [file1.name]);
        file.appendChild(delete_f);
        file.style.borderRadius = one + 'px';
        file.style.backgroundColor = 'white';
        file.style.border = 'solid medium black';
        file.style.width = 'auto';
        file.style.height = 'auto';
        file.style.margin = one + 'px auto';
        file.className = 'selector';
        div.appendChild(file);
        ch_a(file1, file);
        var text12 = document.createElement('a');
        text12.innerText = 'More info';
        text12.style.display = 'inline-block';
        text12.style.paddingLeft = one + 'px';
        text12.title = 'Show info';
        text12.href = '#';
        text12.style.fontSize = one + 'px';
        var info = 'File name: ' + file1.name + '\nSize: ' + formatSizeUnits(file1.b) + '\nType: ' + file1.type;
        text12.onclick = carry(alert, [info]);
        file.appendChild(text12);
    }
}

function send_to_server(json, to_go) {
    var a = document.location.protocol;
    var b = document.location.host;
    fetch(a + '//' + b + to_go,
        {
            method: 'post',
            body: JSON.stringify(json)
        })
        .then(response => response.json())
        .then(json => {
            ref(json, a, b);
        })
}

function click(go) {
    document.getElementById('files').innerHTML = '';
    PATH.push(go);
    var json = {
        path: get_path()
    }
    send_to_server(json, '/get_my_files');
    document.getElementById('path').innerText = get_path();
}

function load() {
    document.getElementById('all').style.height = (window.innerHeight - window.innerHeight / 100 * 2) + 'px';
    var json = {
        path: '/'
    }
    send_to_server(json, '/get_my_files');
}