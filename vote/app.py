from flask import Flask, request, render_template_string
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form.get('vote')
        if vote:
            redis_client.lpush('votes', vote)
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <title>Vote Confirmation</title>
                </head>
                <body style="background-color: #f0f0f0;">
                    <div class="container mt-5">
                        <div class="alert alert-success" role="alert">
                            Your vote for {{ vote }} has been recorded!
                        </div>
                        <a href="/" class="btn btn-primary">Vote Again</a>
                    </div>
                </body>
                </html>
            ''', vote=vote)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Vote</title>
        </head>
        <body style="background-color: #f0f0f0;">
            <div class="container mt-5">
                <h1 class="text-center">Cast Your Vote</h1>
                <div class="row mt-4">
                    <div class="col-md-6" style="background-color: #ff3333; padding: 20px; border-radius: 10px;">
                        <h3>Dogs</h3>
                        <form method="post" class="mt-3">
                            <input type="hidden" name="vote" value="Dogs">
                            <button type="submit" class="btn btn-light">Vote for Dogs</button>
                        </form>
                    </div>
                    <div class="col-md-6" style="background-color: #3333ff; padding: 20px; border-radius: 10px; color: white;">
                        <h3>Cats</h3>
                        <form method="post" class="mt-3">
                            <input type="hidden" name="vote" value="Cats">
                            <button type="submit" class="btn btn-light">Vote for Cats</button>
                        </form>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
