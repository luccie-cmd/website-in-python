from flask import Flask, redirect, url_for, render_template,  request
app = Flask(__name__)

def setup():
    global usernames
    global passwords
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
                for i in usernames:
                    for j in passwords:
                        if username == i and password == j:
                            return redirect(url_for('login'))
                return redirect(url_for('sign_in'))
            elif request.form.get('sign_up_add') == 'sign up':
                username = request.form.get('username').lower()
                password = request.form.get('password')
                last_email = username
                if username not in usernames:
                    with open('passwords.txt', "r") as password_file:
                        original = password_file.read()
                    with open('passwords.txt', "w") as password_file:
                        password_file.write(original + " " + password)
                    with open('usernames.txt', "r") as username_file:
                        original = username_file.read()
                    with open('usernames.txt', "w") as username_file:
                        username_file.write(original + " " + username)
                    usernames.append(username)
                    passwords.append(password)
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
    app.run(None, 5500, True)