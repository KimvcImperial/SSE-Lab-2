from flask import Flask, render_template, request

app = Flask(__name__)

def process_query(query):
    if query == "dinosaurs":
        ans = "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        ans = "Unknown"
    else:
        ans = "No query provided"
    return f"{ans}"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)

@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    return process_query(query)


