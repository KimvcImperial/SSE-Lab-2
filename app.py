from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def is_prime(n):
    """Returns True if n is a prime number, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def process_query(q):
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    
    elif q == "asteroids":
        return "Asteroids are small rocky bodies orbiting the sun"
    
    elif "plus" in q:
        numbers = list(map(int, re.findall(r"\d+", q)))
        return str(sum(numbers)) if numbers else "No valid numbers found."
    
    elif "largest" in q:
        numbers = [float(num) for num in re.findall(r"\d+(?:\.\d+)?", q)]
        return str(max(numbers)) if numbers else "No valid numbers found."
    
    elif "multiplied" in q:
        numbers = list(map(int, re.findall(r"\d+", q)))
        if len(numbers) == 2:
            return str(numbers[0] * numbers[1])
        return "Expected exactly two numbers for multiplication."
    
    elif "are primes" in q:
        numbers = list(map(int, re.findall(r"\d+", q)))
        primes = [str(num) for num in sorted(numbers) if is_prime(num)]
        return ", ".join(primes) if primes else "No prime numbers found."
    
    elif "minus" in q:
        numbers = list(map(int, re.findall(r"\d+", q)))
        return str(numbers[0] - numbers[1]) if len(numbers) >= 2 else "Two numbers required for subtraction."
    
    elif "to the power of" in q:
        numbers = list(map(int, re.findall(r"\d+", q)))
        if len(numbers) == 2:
            return str(numbers[0] ** numbers[1])
        return "Expected base and exponent for power operation."
    
    else:
        return "Unknown query format."

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
    q = request.args.get("q")
    response = process_query(q) if q else "No query provided."
    return jsonify({"query": q, "response": response})







/*from flask import Flask, render_template, request

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
    return process_query(query)*/
