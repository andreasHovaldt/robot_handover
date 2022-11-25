from threading import Thread


def func1():
    while True:
        print(i)

i = 0
def func2():
    while True:
        print(i)

if __name__ == '__main__':
    a = Thread(target = func1)
    b = Thread(target = func2)
    #a.start()
    b.start()