import tkinter
import socket
from tkinter import *
from threading import Thread
import threading

class KillableThread(threading.Thread):
    def __init__(self, sleep_interval=1):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval

    def run(self):
        while True:
            print("Do Something")

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            #  wake up and handle
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break

        print("Killing Thread")

    def kill(self):
        self._kill.set()


def receive():
    while True:
        try:
            msg=s.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END,msg)
        except:
            print("There is error Receiving Message")

def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg,"utf8"))
    if msg == "#quit":
        if receive_Thread.is_alive():
            print('Still Thread running!!!!!!!!!!!!!!!!!!! Terminating.........')
            t = KillableThread(sleep_interval=5)
            t.start()
            # Every 5 seconds it prints:
            #: Do Something
            t.kill()
            #: Killing Thread
        s.close()
        window.close()


def on_closing():
    my_msg.set("#quit")
    send()

window = Tk()
window.title("Chat Room Application")
window.config(bg="green")

message_frame = Frame(window,height=100,width=100,bg='red')
message_frame.pack()
my_msg=StringVar()
my_msg.set("")

scroll_bar=Scrollbar(message_frame)
msg_list = Listbox(message_frame,height=15,width=100,bg="red",yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT,fill=Y)
msg_list.pack(side=LEFT,fill=BOTH)
msg_list.pack()

label = Label(window,text="Enter the message",fg='blue',font='Aeria',bg='red')
label.pack()
entry_field=Entry(window,textvariable=my_msg,fg='red',width=50)
entry_field.pack()

send_button = Button(window,text="Send",font="Areial",fg="white",command=send)
send_button.pack()

quit_button = Button(window,text="Quit",font="Aerial",fg="white",command=on_closing)
quit_button.pack()

Host='127.0.0.1'
Port=8080

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((Host,Port))

receive_Thread=Thread(target=receive)
receive_Thread.start()
mainloop()