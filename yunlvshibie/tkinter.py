import tkinter as tk
from tkinter import messagebox
import mysql.connector

# 连接MySQL数据库
mydb = mysql.connector.connect(
    host="10.130.243.128",
    user="root",
    password="123456",
    database="qyusers"
)

mycursor = mydb.cursor()

def login():
    username = login_entry.get()
    password = password_entry.get()

    mycursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    if result and result[0] == password:
        messagebox.showinfo("Login", "Login Successful!")
        show_recommendations(username)
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

def register():
    username = register_entry.get()
    password = register_password_entry.get()

    mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    if result:
        messagebox.showerror("Registration Error", "Username already exists")
    else:
        mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mydb.commit()
        messagebox.showinfo("Registration", "Registration Successful! Please log in.")

def show_recommendations(username):
    # 创建推荐系统界面
    recommendations_window = tk.Toplevel(root)
    recommendations_window.title("Music Recommendations for " + username)

    # 听歌识曲按钮
    listen_button = tk.Button(recommendations_window, text="Listen to Music Identification", command=lambda: listen_music(username))
    listen_button.pack()

    # 猜你喜欢按钮
    like_button = tk.Button(recommendations_window, text="Guess What You Might Like", command=lambda: guess_likes(username))
    like_button.pack()

def listen_music(username):
    # 这里可以连接算法实现听歌识曲功能
    messagebox.showinfo("Listen to Music Identification", "This feature is under development.")

def guess_likes(username):
    # 这里可以连接算法实现猜你喜欢功能
    messagebox.showinfo("Guess What You Might Like", "This feature is under development.")

# 创建主窗口
root = tk.Tk()
root.title("Music Recommendation System")

# 登录窗口
login_frame = tk.Frame(root)
login_frame.pack(padx=20, pady=20)

login_label = tk.Label(login_frame, text="Username:")
login_label.grid(row=0, column=0)
login_entry = tk.Entry(login_frame)
login_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, columnspan=2, pady=10)

# 注册窗口
register_frame = tk.Frame(root)
register_frame.pack(padx=20, pady=20)

register_label = tk.Label(register_frame, text="New Username:")
register_label.grid(row=0, column=0)
register_entry = tk.Entry(register_frame)
register_entry.grid(row=0, column=1)

register_password_label = tk.Label(register_frame, text="New Password:")
register_password_label.grid(row=1, column=0)
register_password_entry = tk.Entry(register_frame, show="*")
register_password_entry.grid(row=1, column=1)

register_button = tk.Button(register_frame, text="Register", command=register)
register_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()