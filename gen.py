from tkinter import *
import tkinter.scrolledtext as scrol
import socket
import threading
import mttkinter
import select
from  tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
import time
import random
from queue import Queue
import sys


SERVER_PORT = 8826
SERVER_IP = socket.gethostbyname(socket.gethostname())
SELECT_TIMEOUT = 0.01


class scrolled_button(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.queue = Queue()
        self.ready_to_insert = True
        self.text = Text(self, wrap="none")
        vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=vsb.set, width=10)
        vsb.pack(side="right", fill="y", expand=False)
        self.i =1.0
        self.b_list = []
        self.text.pack(expand=False)

        self.text.configure(state="disabled")
    def insert_group( self , group_name , self_client ) :
        b = Button(self, text=group_name,command = lambda : Clien.click_button(self_client,b['text']))
        b.configure(width=10,bg = "lightgray")
        i = self.get_small_i()
        self.b_list.append((b,i))
        self.queue.put(b)
        return  b
        #instead of +1 creat a tuple list that contains the index (1.0,2.0....) and use the find smalles y to find the smalles index
    def remove_empty(self,group_name):
        for index in range(len(self.b_list)):
            if self.b_list[index][0]['text']==group_name:
                self.b_list[index][0].place_forget()
                del self.b_list[index]
    def insert_group_2(self):
        while(self.ready_to_insert==False):
            time.sleep(1)
        while(not self.queue.empty()):
            try:
                b= self.queue.get()
                index_of_b = [y[0]['text'] for y in self.b_list].index(b['text'])
                index_B_real = self.b_list[index_of_b][1]
                self.text.configure(state="normal")
                self.text.window_create(str(index_B_real), window=b)
                self.text.insert('end', "\n")
                self.text.configure(state="disabled")
            except:
                continue



    def set_ready_to_insert(self,bool):
        self.ready_to_insert=bool


    def get_small_i(self):
        smallest_i = 1.0
        y_valus = [tuple_a[1] for tuple_a in self.b_list]
        for count in range(len(self.b_list)):
            if(smallest_i not in y_valus):
                return  smallest_i
            smallest_i+=1
        return  smallest_i


    def remove_group(self,group_name):
        print(group_name)
        for index in range(len(self.b_list)):
            if self.b_list[index][0]['text']==group_name:
                self.b_list[index][0].destroy()
                del self.b_list[index]
                break

    def get_button_list(self):
        return  self.b_list




class Clien:

    def __init__(self, SERVER_IP,SERVER_PORT):
        self.sock = socket.socket()

        self.group_list = []
        self.Y = 39


        gui_thread = threading.Thread(target = self.gui_loop)

        receive_thread = threading.Thread(target = self.receive)

        self._stop = threading.Event()
        self.name = None

        self.all_names = []
        gui_thread.start()
        receive_thread.start()


    def stopped(self):
        return self._stop.isSet()



    def creat_group(self):
        self.T.set_ready_to_insert(False)
        text_area = scrol.ScrolledText(self.win)
        text_area.config(state='disabled')

        name_group= simpledialog.askstring("name for group" , " Choose a name for the group" , parent = self.win)
        if(name_group==None):
            return
        for group in self.group_list:
            if(group[1]['text']==name_group):
                name_group= self.is_group_legit_name(name_group)
                if(name_group=="CLOSE_GROUP#9436125"):
                    return
        input_area = Text(self.win, height=3)


        self.Y = self.get_small_y()

        group_button_1  = self.T.insert_group(name_group,self)

        del_button = Button(self.win, text="press to del players", command=lambda : self.click_del_button(group_button_1['text']))
        del_button.config(font=("Arial", 10), bg='white')

        leader = self.name
        self.group_list.append((text_area, group_button_1, self.Y,input_area ,[leader],del_button))



        self.sock.send(("CREATE_GRUOP" + "/" + " /" + self.name).encode())
        list_names = self.sock.recv(1024).decode().split("/")
        list_names.remove(self.name)
        frame_choose_name = Toplevel(self.win)
        frame_choose_name.geometry("400x400")
        i=0
        self.check_box_list_var=  []
        self.check_box_list=[]
        for name in list_names:
            x = IntVar()
            check_box = Checkbutton(frame_choose_name,text = name,variable=x, onvalue=1)
            self.check_box_list_var.append(x)
            self.check_box_list.append(check_box)
            check_box.grid(row=i,column=0)
            i=i+1
        if(i!=0):
            Button(frame_choose_name, text=" click to choose users",command=lambda: self.get_check_box(name_group, frame_choose_name,"CREATE_GRUOP_FOR_OTHERS",group_button_1)).grid(row=i, column=0)
        else:
            self.T.set_ready_to_insert(True)
            Button(frame_choose_name, text="NO USERS CONNECTED , PRESS TO PASS ",command = lambda : frame_choose_name.destroy()).grid(row=i, column=0)

    def get_check_box(self,name_group,frame_choose_name,text,group_button_1):
        name_list = ""
        for check_box_var in self.check_box_list_var:
            if(check_box_var.get()>=1):
                name_list= name_list +self.check_box_list[self.check_box_list_var.index(check_box_var)]['text'] +"*"
        frame_choose_name.destroy()
        print(name_list)
        if(name_list==""):
            if(text=="CREATE_GRUOP_FOR_OTHERS"):
                for index in range(len(self.group_list)):
                    if self.group_list[index][1]['text']==name_group:
                        self.group_list[index][0].place_forget()
                        self.T.remove_group(self.group_list[index][1]['text'])
                        self.group_list[index][3].place_forget()
                        self.T.remove_empty(name_group)
                        del self.group_list[index]
                        self.T.set_ready_to_insert(True)
                        break
            elif(text =='DEL_MEMBER_OF_GROUP'):
                pass

        else:
            if(group_button_1 != None):
                print(name_group+"please work")
                self.group_list[len(self.group_list)-1] =self.group_list[len(self.group_list)-1]+(name_list.split("*")[0:len(name_list.split("*"))-1],)
                print(self.group_list[len(self.group_list)-1][6])
                self.T.set_ready_to_insert(True)
                self.T.insert_group_2()

            self.sock.send(str(text + "/"+ name_list[0:len(name_list)-1]+"/"+name_group).encode())
            if(text == 'DEL_MEMBER_OF_GROUP'):
                index = [y[1]['text'] for y in self.group_list].index(self.Current_Screen)
                print(name_list)
                name_list = name_list.split("*")
                name_list = name_list[0:len(name_list)-1]
                for name in name_list:
                    print(self.group_list[index][6])
                    print(" list")
                    print(name)
                    print("name")
                    self.group_list[index][6].remove(name)


    def is_group_legit_name(self,name_group):
        is_legit = False
        while(True):
            name_group = simpledialog.askstring("nickname", " enter other name", parent=self.win)
            if(name_group==None):
                return "CLOSE_GROUP#9436125"
            for group in self.group_list:
                if (group[1]['text'] == name_group):
                    is_legit=False
                    break
            is_legit=True
            if(is_legit):
                return name_group

    def is_legit_name(self):
        while(True):
            if(self.name==None):
                self._stop.set()
                return "stop_code"
            time.sleep(0.5)
            self.sock.send(("NAME_SOCK" + "/" + " /" + self.name).encode())
            data = self.sock.recv(1024).decode()
            print(data)
            if (data == "NAME_SOCK"):
                self.name = simpledialog.askstring("nickname", " enter other name", parent=self.win)
            else:
                break

    def gui_loop(self):
        self.win = Tk()



        self.win.configure(bg="lightgray")
        self.win.geometry("1000x700")
        self.win.resizable(False, False)            # setting up the main screen
        self.win.withdraw()

        self.sock.connect((SERVER_IP, SERVER_PORT)) # bug needs to be fixed : i cannot check if name in name list because i dont have acces , i need to change the way i bring name of client to the server

        self.name = simpledialog.askstring("nickname", " enter name", parent=self.win)
        if(self.name==None):
            self._stop.set()
            self.sock.send("CLOSE_CONNECTION".encode())
            time.sleep(3)
            self._stop.set()
            return
        self.sock.send(("NAME_SOCK" + "/" + " /" + self.name).encode())
        d= self.sock.recv(1024).decode()
        print(d + " capable name")
        if( d == "NAME_SOCK"):
            b= self.is_legit_name()
            if(b=="stop_code"):
                self.sock.send("CLOSE_CONNECTION".encode())
                time.sleep(3)
                self._stop.set()
                return
        print("--------------------- "+self.name+ "-------------------------------")
        self.win.deiconify()
        self.Current_Screen = ""# name of group
        self.Current_Text = scrol.ScrolledText(self.win)# text area     # set up variables to know the current gruop
        self.Current_input =Text(self.win)# text input box
        self.Current_del = Button(self.win)
        self.Current_chat_label = Label(self.win,text="")
        self.Current_chat_label.config(bg="lightgray")


        # creating the scrolled text
        self.T = scrolled_button(self.win)
        self.T.pack(side=LEFT, expand=False)
        self.T.place(x=0, y=100)





        self.chat_label = Label(self.win, text="chat: "+self.name, bg="white")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=1, pady=1)
        self.chat_label.place(x=0, y=0)

        self.msg_label = Label(self.win, text="Msseage ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)
        self.msg_label.place(x=400, y=418)


        self.send_button = Button(self.win, text="Send", command=self.send_button_f)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.send_button.place(x=400, y=510)


        self.group_creat = Button(self.win, text="group_create", command=self.creat_group)
        self.group_creat.config(font=("Arial", 12))
        self.group_creat.pack(padx=20, pady=5)
        self.group_creat.place(x=700, y=510)

        # self.name_entry = Entry(self.win)
        # self.name_entry.pack(padx=20, pady=5)
        # self.name_entry.place(x=700, y=600)

        # self.name_button = Button(self.win, text="Click me to update name", command=self.update_name)
        # self.name_button.config(font=("Arial", 12))
        # self.name_button.pack(padx=20, pady=5)
        # self.name_button.place(x=700, y=620)




        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()
        if (self.stopped()):
            print("sys1")
            return



    def get_small_y(self):
        smallest_y = 39
        y_valus  = [tuple_a[2] for tuple_a in self.group_list]
        for count in range(len(self.group_list)):
            if(smallest_y not in y_valus):
                return  smallest_y
            smallest_y+=39
        return  smallest_y

    # def update_name(self):
    #
    #     name = simpledialog.askstring("nickname", " enter name", parent=self.win)
    #     self.name = name
    #     self.chat_label['text'] = "chat: "+self.name


    def click_del_button(self,name_group):

        for group in self.group_list:
            if group[1]['text'] == name_group:
                list_names = group[6]
                break
        frame_choose_name = Toplevel(self.win)
        frame_choose_name.geometry("400x400")
        i = 0
        self.check_box_list_var = []
        self.check_box_list = []
        for name in list_names:
            x = IntVar()
            check_box = Checkbutton(frame_choose_name, text=name, variable=x, onvalue=1)
            self.check_box_list_var.append(x)
            self.check_box_list.append(check_box)
            check_box.grid(row=i, column=0)
            i = i + 1
        if (i != 0):
            Button(frame_choose_name, text=" click to choose users",command=lambda: self.get_check_box(name_group, frame_choose_name,"DEL_MEMBER_OF_GROUP",None)).grid(row=i, column=0)
        else:
            Button(frame_choose_name, text="NO USERS CONNECTED , PRESS TO PASS ",command=lambda: frame_choose_name.destroy()).grid(row=i, column=0)




    def send_button_f(self):
        text =self.Current_input.get('1.0', END)
        self.Current_input.delete('1.0', 'end')
        self.Current_Text.config(state='normal')
        new_name  = self.name
        index = [y[1]['text'] for y in self.group_list].index(self.Current_Screen)
        if (self.name in self.group_list[int(index)][4]):
            new_name = "@" + self.name
        self.Current_Text.insert('end',str(datetime.now().strftime("%H:%M:%S")+" " +  new_name + " : " + text +"\r\n"))      # show message on screen
        self.Current_Text.yview('end')
        self.Current_Text.config(state='disabled')

        self.sock.send(("SEND"+"/"+str(datetime.now().strftime("%H:%M:%S"))+"/"+new_name+"/"+self.Current_Screen+ "/"+ text).encode())


    def click_button(self,text):
        for group in self.group_list:
            if group[1]['text'] == text:
                if self.Current_Screen!=text:
                    self.Current_Text.place_forget()
                    self.Current_del.place_forget()
                    group[0].pack(padx=2, pady=2)
                    group[0].config(state='disabled')
                    group[0].place(x=107, y=30)
                    group[1].config(bg = 'lightgray')

                    self.Current_Screen = group[1]['text']
                    self.Current_Text =group[0]
                    self.Current_input.place_forget()
                    self.Current_input = group[3]
                    group[3].pack(padx=20, pady=5)
                    group[3].place(x=107, y=450)
                    if(self.name in group[4]):
                        self.Current_del = group[5]
                        self.Current_del.pack()
                        self.Current_del.place(x=650, y=600)
                    self.Current_chat_label['text'] = self.Current_Screen
                    self.Current_chat_label.place(x=400,y=0)

                    break

    def receive(self):
        while True:
            rlist, wlist, xlist = select.select([self.sock], [], [], 0.01)
            if self.sock in rlist:
                if(self.stopped()):
                    break
                data = self.sock.recv(1024).decode()
                print(data + " : data from server")
                data = data.split("/")                              #after i get massege
                command = data[0]
                time = data[1]
                name = data[2]
                group_name = data[3]
                msg= data[4]
                if(command == "NAME_SOCK"):
                    self.sock.send(("NAME_SOCK"+"/"+ " /"+self.name).encode())
                elif(command=="CREATE_GRUOP_FOR_OTHERS"):
                    self.creat_group_from_sock(group_name,data)
                elif(command=="DEL_MEMBER_OF_GROUP"):
                    self.del_group_from_sock(group_name, data)
                elif (command == "quit"):
                    self.quit_chat(data)
                else:
                    for pack in self.group_list:
                        if pack[1]['text'] == group_name:
                            pack[0].config(state='normal')
                            pack[0].insert('end',time+" "+name+ ":"+ msg + "\r\n")  # after i send message
                            pack[0].yview('end')
                            pack[0].config(state='disabled')
                            if pack[1]['text'] !=self.Current_Screen:
                                pack[1].config(bg='red')
                            break
        print("sys2")
        return



    def creat_group_from_sock(self,group_name,data):
        text_area = scrol.ScrolledText(self.win)
        text_area.config(state='disabled')

        input_area = Text(self.win, height=3)

        group_button_1 = self.T.insert_group(group_name,self)
        self.T.insert_group_2()
        list_names = data[6].split("*")
        list_names.append(data[5])
        print(list_names)
        print(type(list_names))
        self.group_list.append((text_area, group_button_1, self.Y, input_area,[data[5]],list_names))# data[5] leader



    def quit_chat(self,data):
        for group in self.group_list:
            print(len(group))
            print(data[2])
            print(group[5])
            if(len(group)==7):
                if(data[2] in group[6]):
                    group[0].config(state='normal')
                    group[0].insert('end',data[4]+"\r\n")
                    group[6].remove(data[2])
                    group[0].yview('end')
                    print(self.Current_Screen)

                    if(self.Current_Screen!=group[1]['text']):
                        group[1].config(bg='red')
                    group[0].config(state='disabled')
                    print(group[1]['text'])
            if(len(group)==6):
                if (data[2] in group[5]):
                    group[0].config(state='normal')
                    group[0].insert('end', data[4] + "\r\n")
                    group[5].remove(data[2])
                    group[0].yview('end')
                    print(self.Current_Screen)

                    if (self.Current_Screen != group[1]['text']):
                        group[1].config(bg='red')
                    group[0].config(state='disabled')
                    print(group[1]['text'])


    def del_group_from_sock(self, group_name, data):
        for group in self.group_list:
            if group[1]['text'] == group_name:
                print(group_name+self.name)
                self.T.remove_group(group_name)
                group[0].place_forget()
                group[3].place_forget()
                self.group_list.remove(group)
                if(self.Current_Screen==group_name):
                    self.Current_chat_label['text']=""
                break


    def write(self):
        pass

    def stop(self):

        self.stop_p = Tk()
        self.stop_p.withdraw()
        if messagebox.askyesno("quit chat","are u sure you want to quit?",parent = self.stop_p):
            self._stop.set()
            self.stop_p.destroy()
            self.win.destroy()
            self.win.quit()

            self.sock.send((("quit"+"/"+str(datetime.now().strftime("%H:%M:%S")+"/"+self.name+"/")).encode()))
            self.sock.close()




client = Clien(SERVER_IP, SERVER_PORT)