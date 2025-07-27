from flask import Flask, render_template_string
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(dbname="voting", user="postgres", password="postgres", host="db")

@app.route('/')
def result():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT vote, COUNT(*) FROM votes GROUP BY vote;")
    results = cur.fetchall()
    conn.close()

    total_votes = sum(count for _, count in results) if results else 1  # Avoid division by zero
    dogs_votes = next((count for vote, count in results if vote == "Dogs"), 0)
    cats_votes = next((count for vote, count in results if vote == "Cats"), 0)
    dogs_percent = (dogs_votes / total_votes * 100) if total_votes > 0 else 0
    cats_percent = (cats_votes / total_votes * 100) if total_votes > 0 else 0

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Results</title>
        </head>
        <body style="background-color: #f0f0f0;">
            <div class="container mt-5">
                <h1 class="text-center">Voting Results</h1>
                <div class="row mt-4">
                    <div class="col-md-6" style="background-color: #ff3333; padding: 20px; border-radius: 10px;">
                        <h3>Dogs</h3>
                        <p>Votes: {{ dogs_votes }} ({{ '%.1f' % dogs_percent }}%)</p>
                    </div>
                    <div class="col-md-6" style="background-color: #3333ff; padding: 20px; border-radius: 10px; color: white;">
                        <h3>Cats</h3>
                        <p>Votes: {{ cats_votes }} ({{ '%.1f' % cats_percent }}%)</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', dogs_votes=dogs_votes, cats_votes=cats_votes, dogs_percent=dogs_percent, cats_percent=cats_percent)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
