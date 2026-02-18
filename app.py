from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (short TEXT, long TEXT)')
    conn.commit()
    conn.close()

# Generate short code
def generate_short():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short()
        
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('INSERT INTO urls VALUES (?, ?)', (short_code, long_url))
        conn.commit()
        conn.close()
        
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT long FROM urls WHERE short=?', (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    return "URL not found!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
