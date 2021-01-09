import subprocess

command = 'Hello'
while command != ['Exit']:
    commands = []
    z = 1
    command = input(f'Команда_{z}: ').split()
    if command != ['Exit']:
        while command != []:
            commands.append(command)
            z += 1
            command = input(f'Команда_{z}: ').split()
        for com in commands:
            try:
                print('\n\n=============================================\n')
                print(f'{com[0]}:')
                subprocess.call(com)
            except FileNotFoundError:
                print(f'Ошибка команды "{com[0]}" не существует!')
            print('\n=============================================\n\n')

