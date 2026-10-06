from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email")
    segregation = request.form.get("segregation")
    waste = request.form.get("waste")
    suggestion = request.form.get("suggestion")

    reuse = "Yes" if request.form.get("reuse") else "No"
    recycle = "Yes" if request.form.get("recycle") else "No"
    segregate = "Yes" if request.form.get("segregate") else "No"
    compost = "Yes" if request.form.get("compost") else "No"

    with open("survey_responses.txt", "a") as file:

        file.write("Name: " + str(name) + "\n")
        file.write("Email: " + str(email) + "\n")
        file.write("Segregates Waste: " + str(segregation) + "\n")
        file.write("Most Produced Waste: " + str(waste) + "\n")

        file.write("Reuse Materials: " + reuse + "\n")
        file.write("Recycle: " + recycle + "\n")
        file.write("Segregate Waste: " + segregate + "\n")
        file.write("Compost Organic Waste: " + compost + "\n")

        file.write("Suggestion: " + str(suggestion) + "\n")

        file.write("----------------------------------\n")

    return "Survey submitted successfully!"


@app.route("/responses")
def responses():

    password = request.args.get("password")

    if password != "zero123":
        return "Access denied"

    try:
        with open("survey_responses.txt", "r") as file:
            data = file.read()

        return "<pre>" + data + "</pre>"

    except FileNotFoundError:
        return "No survey responses yet."


if __name__ == "__main__":
    app.run(debug=True)
