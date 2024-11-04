from flask import Flask, render_template, request
import re

import requests


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


def process_query(query):
    if query == "dinosaurs":
        ans = "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        ans = "Unknown"

    elif "plus" in query:
        numbers = list(map(int, re.findall(r"\d+", query)))
        ans = str(sum(numbers)) if numbers else "No valid numbers found."

    elif "largest" in query:
        numbers = [float(num) for num in re.findall(r"\d+(?:\.\d+)?", query)]
        ans = str(max(numbers)) if numbers else "No valid numbers found."

    elif "multiplied" in query:
        numbers = list(map(int, re.findall(r"\d+", query)))
        if len(numbers) == 2:
            ans = str(numbers[0] * numbers[1])
        else:
            ans = "Expected exactly two numbers for multiplication."

    elif "both a square and a cube" in query:
        numbers = [int(num) for num in re.findall(r"\d+", query)]
        valid_numbers = [
            str(num) for num in numbers if round(num ** (1 / 6)) ** 6 == num
        ]
        ans = (
            ", ".join(valid_numbers)
            if valid_numbers
            else "No numbers found that are both a square and a cube."
        )

    elif "are primes" in query:
        numbers = [int(num) for num in re.findall(r"\d+", query)]
        primes = [str(num) for num in numbers if is_prime(num)]
        ans = ", ".join(primes) if primes else "No prime numbers found."

    elif "minus" in query:
        numbers = list(map(int, re.findall(r"\d+", query)))
        ans = (
            str(numbers[0] - numbers[1])
            if len(numbers) >= 2
            else "Two numbers required for subtraction."
        )

    elif "to the power of" in query:
        numbers = list(map(int, re.findall(r"\d+", query)))
        if len(numbers) == 2:
            ans = str(numbers[0] ** numbers[1])
        else:
            ans = "Expected base and exponent for power operation."

    else:
        ans = "No query provided"  # Handling unknown queries

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


@app.route("/github")
def index():
    return render_template("indexA.html")


@app.route("/greet", methods=["POST"])
def greet():
    username = request.form["username"]
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code == 200:
        repos = response.json()
        repo_data = []

        # Fetching commits for each repository
        for repo in repos:
            repo_info = {"name": repo["full_name"], "commits": []}
            commits_response = requests.get(
                f"https://api.github.com/repos/{username}/{repo['name']}/commits"
            )

            if commits_response.status_code == 200:
                commits = commits_response.json()
                for commit in commits:
                    commit_info = {
                        "hash": commit["sha"],
                        "author": commit["commit"]["author"]["name"],
                        "date": commit["commit"]["author"]["date"],
                        "message": commit["commit"]["message"],
                    }
                    repo_info["commits"].append(commit_info)

            repo_data.append(repo_info)

        return render_template("github.html", username=username, repo_data=repo_data)
    else:
        return render_template(
            "github.html",
            username=username,
            repo_data=[],
            error="User not found or has no repositories.",
        )


if __name__ == "__main__":
    app.run(debug=True)


"""from flask import Flask, render_template, request

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
    return process_query(query)"""
