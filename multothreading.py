import threading

def x():
    while True:
        print("inx")

def main():
    t1 = threading.Thread(target=x)
    t1.start()

    while True:
        print("main")
        t1.join()

if __name__ == "__main__":

    main()