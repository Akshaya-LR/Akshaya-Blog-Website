from flask import Flask, render_template, request
import requests
import smtplib
import os


app = Flask(__name__)


message = "Successfully sent your message!!"
sub_msg = "Have anymore questions?"
contact_head = "Message Me!"
contact_sub = "Send me a quick message!"

get_post = os.environ.get("API")
blog_p = requests.get(get_post)
posts = blog_p.json()


email = os.environ.get("EMAIL")
pwd = os.environ.get("PWD")


@app.route('/')
def home():
    return render_template('index.html', blogpost=posts)


@app.route('/post/<int:num>')
def post(num):
    post_requested = None
    # print(posts['id'])
    for posting in posts:
        if posting['id'] == num:
            # print(post['title'])
            post_requested = posting
            # print(post_requested)
        # print(post_requested)
    return render_template('post.html', heading=post_requested["title"], sub_heading=post_requested["subtitle"],
                           posts=post_requested)


@app.route('/about')
def about():
    return render_template('about.html')


def email_me(name, mail, phone, msg):
    email_message = f"Subject:New Message from Blog Website - User\n\nName: {name}\nEmail: {mail}\nPhone: {phone}\nMessage:{msg}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(email, pwd)
        connection.sendmail(email, email, email_message)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_data = request.form
        print(user_data["name"])
        email_me(user_data["name"], user_data["email"], user_data["phone_number"], user_data["message"])
        return render_template('contact.html', heading=message, sub_heading=sub_msg)
    return render_template('contact.html', heading=contact_head, sub_heading=contact_sub)


if __name__ == '__main__':
    app.run(debug=True)