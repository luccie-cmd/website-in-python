from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
emails = ["test@gmail.com"]
passwords = ["test1234"]

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<h1>" + str(e) + "</h1>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('sign_in') == 'sign in':
            return redirect(url_for('sign_in'))
        elif request.form.get('login') == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            for i in emails:
                for j in passwords:
                    if email == i and password == j:
                        return redirect(url_for('login'))
            return redirect(url_for('sign_in'))
        else:
            return redirect(url_for('False_Button'))
    return render_template("index.html")

@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

@app.route('/False_Button')
def False_Button():
    return render_template("False_Button.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(None, 5500, True)