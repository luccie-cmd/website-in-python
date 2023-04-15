from flask import Flask, redirect, url_for, render_template, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from json import dump, load
app = Flask(__name__)
#replace this with your computers ip addres
host_addr: str = "192.168.2.18"

def setup():
    global usernames
    global passwords
    global users
    users = []
    try:    
        with open("usernames.txt") as username_file:
            usernames = username_file.read().split()
    except FileNotFoundError:
        with open("usernames.txt", "w") as username_file:
            print("INFO: username FILE MADE")
    try:
        with open("passwords.txt") as passwords_file:
            passwords = passwords_file.read().split()
    except FileNotFoundError:
        with open("passwords.txt", "w") as passwords_file:
            print("INFO: PASSWORD FILE CREATED")
    for n in usernames:
        for p in passwords:
            users.append(User(n, p))
            
class User:
    global data, original_data
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        for u in users:
            data.append({"name": u.get_name(), "password": u.get_pass()})
        with open("users.json", "w") as f:
            f.flush()
            dump(data, f)
        original_data = data
    def add_to_db(self):
        with open('passwords.txt', "r") as password_file:
            original = password_file.read()
            with open('passwords.txt', "w") as password_file:
                password_file.write(original + " " + self.password)
            with open('usernames.txt', "r") as username_file:
                original = username_file.read()
            with open('usernames.txt', "w") as username_file:
                username_file.write(original + " " + self.username)
        usernames.append(self.get_name())
        passwords.append(self.get_pass())
        original_data.append({"name": u.get_name(), "password": u.get_pass()})
        with open("users.json", "w") as f:
            f.flush()
            dump(original_data, f)
    def get_pass(self):
        return self.password
    def get_name(self):
        return self.username
            
class Errors:
    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>" + str(e) + "</h1>"
    
class Routes:
    global last_email
    last_email = None
        
    @app.route('/', methods=['GET', 'POST'])
    def index():
        global last_email
        last_email = None
        if request.method == 'POST':
            if request.form.get('sign_in') == 'sign in':
                return redirect(url_for('sign_in'))
            elif request.form.get('sign_up_page') == 'sign up':
                return redirect(url_for('sign_up'))
            elif request.form.get('login') == 'login':
                username = request.form.get('username').lower()
                password = request.form.get('password')
                last_email = username
                for u in users:
                    if username == u.get_name() and check_password_hash(u.get_pass(), password):
                        return redirect(url_for('login'))
                return redirect(url_for('sign_in'))
            elif request.form.get('sign_up_add') == 'sign up':
                username = request.form.get('username').lower()
                password = request.form.get('password')
                hashed_password = generate_password_hash(password)
                last_email = username
                if username not in usernames:
                    users.append(User(username, hashed_password))
                    for u in users:
                        u.add_to_db()
                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('sign_in'), 302)
            else:
                return redirect(url_for('False_Button'))
        return render_template("index.html")

    @app.route('/sign_in')
    def sign_in():
        return render_template("sign_in.html")

    @app.route('/sign_up')
    def sign_up():
        return render_template("sign_up.html")

    @app.route('/False_Button')
    def False_Button():
        return render_template("False_Button.html")

    @app.route("/login")
    def login():
        if last_email == None:
            return redirect(url_for("sign_in"))
        return render_template("login.html", name=last_email)

if __name__ == '__main__':
    setup()
    app.run(host_addr, 5500, True)