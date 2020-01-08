from _winapi import CREATE_NEW_CONSOLE
from subprocess import Popen

proc_list = []

while True:
    user = input("Запустить несколько клиентов и сервер (s) / Закрыть всё (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':
        clients = int(input("Сколько клиентов запустить? "))

        for _ in range(1):
            proc_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
            print('Запуск сервера')

        for _ in range(clients):
            proc_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))
            print('Запуск клиентов')
    elif user == 'x':
        for process in proc_list:
            process.kill()
        proc_list.clear()
