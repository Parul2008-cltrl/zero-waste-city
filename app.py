import os
from flask import Flask, request
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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

    supabase.table("survey_responses").insert({
        "name": name,
        "email": email,
        "segregation": segregation,
        "waste": waste,
        "reuse": reuse,
        "recycle": recycle,
        "segregate": segregate,
        "compost": compost,
        "suggestion": suggestion
    }).execute()

    return "Survey submitted successfully!"


@app.route("/responses")
def responses():

    password = request.args.get("password")

    if password != "zero123":
        return "Access denied"

    result = (
        supabase
        .table("survey_responses")
        .select("*")
        .order("created_at")
        .execute()
    )

    if not result.data:
        return "No survey responses yet."

    data = ""

    for row in result.data:
        data += "Name: " + str(row.get("name")) + "\n"
        data += "Email: " + str(row.get("email")) + "\n"
        data += "Segregates Waste: " + str(row.get("segregation")) + "\n"
        data += "Most Produced Waste: " + str(row.get("waste")) + "\n"
        data += "Reuse Materials: " + str(row.get("reuse")) + "\n"
        data += "Recycle: " + str(row.get("recycle")) + "\n"
        data += "Segregate Waste: " + str(row.get("segregate")) + "\n"
        data += "Compost Organic Waste: " + str(row.get("compost")) + "\n"
        data += "Suggestion: " + str(row.get("suggestion")) + "\n"
        data += "----------------------------------\n"

    return "<pre>" + data + "</pre>"


if __name__ == "__main__":
    app.run(debug=True)
