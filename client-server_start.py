from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []

while True:
    user = input("Запустить несколько клиентов и сервер (s) / Закрыть всё (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':    
        for _ in range(1):
            p_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
            print('Запуск сервера')
        for _ in range(2):
            p_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))
            print('Запуск клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
