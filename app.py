from flask import Flask, redirect, url_for, render_template,  request

app = Flask(__name__)
try:    
    with open("emails.txt") as email_file:
        emails = email_file.read().split()
except FileNotFoundError:
    with open("emails.txt", "w") as email_file:
        print("INFO: EMAIL FILE MADE")
        emails = []
try:
    with open("passwords.txt") as passwords_file:
        passwords = passwords_file.read().split()
except FileNotFoundError:
    with open("passwords.txt", "w") as passwords_file:
        print("INFO: PASSWORD FILE CREATED")
        passwords = []

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<h1>" + str(e) + "</h1>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('sign_in') == 'sign in':
            return redirect(url_for('sign_in'))
        elif request.form.get('sign_up_page') == 'sign up':
            return redirect(url_for('sign_up'))
        elif request.form.get('login') == 'login':
            global email, password
            email = request.form.get('email')
            password = request.form.get('password')
            for i in emails:
                for j in passwords:
                    if email == i and password == j:
                        return redirect(url_for('login'))
            return redirect(url_for('sign_in'))
        elif request.form.get('sign_up_add') == 'sign up':
            email = request.form.get('email')
            password = request.form.get('password')
            if email not in emails:
                with open('passwords.txt', "r") as password_file:
                    original = password_file.read()
                with open('passwords.txt', "w") as password_file:
                    password_file.write(original + " " + password)
                with open('emails.txt', "r") as email_file:
                    original = email_file.read()
                with open('emails.txt', "w") as email_file:
                    email_file.write(original + " " + email)
                return redirect(url_for('login'))
            else:
                return redirect(url_for('sign_in'), 302)
        else:
            return redirect(url_for('False_Button'))
    return render_template("index.html")

@app.route('/sign_in')
def sign_in():
    print(emails, passwords)
    return render_template("sign_in.html")

@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@app.route('/False_Button')
def False_Button():
    return render_template("False_Button.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(None, 5500, True)