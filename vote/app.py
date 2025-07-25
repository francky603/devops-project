from flask import Flask, render_template, request
import redis
import ssl
app = Flask(__name__)
r = redis.Redis(host="redis", port=6379, db=0)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        choice = request.form.get("vote")
        if choice in ["Dogs", "Cats"]:
            r.rpush("votes", choice)
        return render_template("index.html")
    return render_template("index.html")
if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/app/server.crt", "/app/server.key")
    app.run(host="0.0.0.0", port=443, ssl_context=context)
