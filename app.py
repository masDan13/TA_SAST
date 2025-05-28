from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Hardcoded credentials (kerentanan)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

@app.route('/')
def index():
    return "Welcome to the vulnerable Flask app!"

# SQL Injection vulnerability
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return "Login Successful!"
        else:
            return "Login Failed."
    return '''
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    '''

# XSS vulnerability
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return render_template_string(f"<h1>Hello, {name}!</h1>")

if __name__ == '__main__':
    app.run(debug=True)
