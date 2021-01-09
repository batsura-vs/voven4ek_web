import subprocess
import random
from time import sleep


def check():
    try:
        subprocess.check_call(["ping", "-c 1", "www.google.ru"])
        return True
    except subprocess.CalledProcessError:
        return False


def get_mac():
    mac1 = [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac1))


z = 0
while True:
    if check() is False:
        for x in range(1, 4):
            if check() is False:
                z += 1
                print(z)
                if z >= 3:
                    mac = get_mac()
                    subprocess.call(['ifconfig', 'wlp2s0', 'down'])
                    subprocess.call(['ifconfig', 'wlp2s0', 'hw', 'ether', mac])
                    subprocess.call(['ifconfig', 'wlp2s0', 'up'])
                    print('======================')
                    print('\n\nMAC адрес был изменён!')
                    print('Вот ваш mac: ' + str(mac) + '\n\n')
                    print('======================')
                    z = 0
                sleep(3)
            else:
                z = 0
                break
    else:
        z = 0
    sleep(10)

