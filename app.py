import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://maud:test@cluster0.p4vc7.mongodb.net/microblog?retryWrites=true&w=majority",
                        ssl=True, ssl_cert_reqs="CERT_NONE")
    app.db = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("message")
            formatted_dates = datetime.date.today().strftime("%Y-%m-%d")
            app.db.entries.insert(
                {"content": entry_content, "date": formatted_dates})

        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.datetime.strptime(
                    entry['date'], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)


    @app.route("/hello")
    def first_page():
        name = "Maud"
        template_name = "test"
        kwargs = {
            "name": name,
            "template_name": template_name
        }
        return render_template("test.html", **kwargs)
    return app
