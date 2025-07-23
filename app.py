from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            movie TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            seats INTEGER NOT NULL
        )
    ''')
    conn.close()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# List of movies
@app.route('/movies')
def movies():
    movies = ['Bahubali', 'Pournami', 'Thandel', 'Amaran', 'Kannappa']
    return render_template('movies.html', movies=movies)

# Booking form for selected movie
@app.route('/book/<movie>')
def book(movie):
    return render_template('book.html', movie=movie)

# Handle booking submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    movie = request.form['movie']
    date = request.form['date']
    time = request.form['time']
    seats = int(request.form['seats'])

    conn = sqlite3.connect('database.db')
    conn.execute('INSERT INTO bookings (name, movie, date, time, seats) VALUES (?, ?, ?, ?, ?)',
                 (name, movie, date, time, seats))
    conn.commit()
    conn.close()

    return render_template('success.html', name=name, movie=movie, date=date, time=time, seats=seats)

# Admin view to see all bookings
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

# Run the app
if __name__ == '__main__':
    init_db()
    print("✅ Flask app starting at http://127.0.0.1:5000")
    app.run(debug=True)
