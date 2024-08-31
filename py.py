from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Route to display the login form
@app.route('/')
def index():
    return '''
    <form method="post" action="/login">
      <div class="container">
        <h1>Log In</h1>
        <hr>
        <label for="email"></label>
        <input type="text" placeholder="Enter Email" name="email" required>
        <label for="psw"></label>
        <input type="password" placeholder="Enter Password" name="psw" required>
        <div class="clearfix">
          <button type="submit" class="loginbtn">Log In</button>
        </div>
      </div>
    </form>
    '''

# Route to handle form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['psw']
    
    # Save to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return redirect(url_for('index'))  # Redirect to a success page or home page
    except sqlite3.IntegrityError:
        # Handle duplicate email case or other errors
        return 'Email already registered or error occurred.'
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
