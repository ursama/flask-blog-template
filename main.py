from flask import Flask, render_template, request
from email.header import Header
import requests
import smtplib

SEND_TO = "Your mail"
SEND_FROM = "Your mail"

app = Flask(__name__)
response = requests.get(url="https://api.npoint.io/32870786301096dd67ce")
response.raise_for_status()
posts_response = response.json()


@app.route('/')
def home():
    header_title = "Home"
    return render_template("index.html", title=header_title, posts=posts_response)


@app.route("/about")
def about():
    header_title = "About"
    return render_template("about.html", title=header_title)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=SEND_FROM, password="password for 'SEND_FROM' email")
        connection.sendmail(
            from_addr=SEND_FROM,
            to_addrs=SEND_TO,
            msg=f"Subject:You got a new message!\n\n"
                f"A message from: {request.form['name']}\n"
                f"Email: {request.form['email']}\n"
                f"Phone: {request.form['phone']}\n"
                f"Message: {request.form['message']}".encode('utf-8')
        )
        connection.close()

    header_title = "Contact"
    return render_template("contact.html", title=header_title)


@app.route("/post/<post_id>")
def post(post_id):
    searched_post = posts_response[0]
    for text in posts_response:
        if text["id"] == int(post_id):
            print(text)
            searched_post = text
    header_title = searched_post["title"]

    return render_template("post.html", title=header_title, post=searched_post)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
