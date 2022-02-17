import build_sql
from tkinter import *

acp_state = False

acp_window = Tk()

def login(badge, password):
    if len(badge) == 6:
        print(password)

def acp_log_in():
    acp_login = Tk()
    acp_login.title('ACP - Login')
    acp_login.geometry('250x150')
    acp_login.resizable(0, 0)

    content_header = Frame(acp_login)
    content_header.pack()
    label = Label(content_header, text='Please login to continue...')
    label.pack(pady=10)

    content = Frame(acp_login)
    content.pack()

    badge_lbl = Label(content, text='Badge No.:')
    badge = Entry(content)
    password_lbl = Label(content, text='Password:')
    password = Entry(content, show='*')

    badge.grid(row=0, column=1, pady=(10, 0))
    badge_lbl.grid(row=0, column=0)
    password.grid(row=1, column=1)
    password_lbl.grid(row=1, column=0)

    error_content = Frame(acp_login)
    error_content.pack()

    submit = Button(error_content, text='Enter', command=lambda: login(badge.get(), password.get()))
    submit.pack(pady=(5,0))

    error_lbl = Label(error_content, text='')
    error_lbl.pack()

if not acp_state:
    acp_window.title('ACP')
    acp_window.geometry('200x100')
    acp_window.resizable(0, 0)

    login_btn = Button(acp_window, text="Log In", command=acp_log_in)
    login_btn.place(relx=0.5, rely=0.5, anchor=CENTER)


elif acp_state:
    acp_window.title('ACP - Select')
    acp_window.geometry('500x500')
    acp_window.resizable(0, 0)

mainloop()