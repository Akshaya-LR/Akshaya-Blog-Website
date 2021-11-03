# Import the required Packages
from flask import Flask, render_template, request
import requests
import smtplib
import os
# from dotenv import load_dotenv

# load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Variables used
message = "Successfully sent your message!!"
sub_msg = "Have anymore questions?"
contact_head = "Contact Me!"
contact_sub = "Send me a quick message!"

# API for the blog posts
get_post = "https://api.npoint.io/b9110dd9f30a652d5da0"
blog_p = requests.get(get_post)
posts = blog_p.json()

# Use environment variables for personal info
email = os.environ.get("EMAIL")
pwd = os.environ.get("PWD")

# email = "akshayasharma0104@gmail.com"
# pwd = "Merry@12"

# Home page route
@app.route('/')
def home():
    return render_template('index.html', blogpost=posts)


# Blog post route
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


# About page route
@app.route('/about')
def about():
    return render_template('about.html')


# Send Email function from Contact page using SMTP
def email_me(name, mail, phone, msg):
    email_message = f"Subject:New Message from Blog Website - User\n\nName: {name}\nEmail: {mail}\nPhone: {phone}\nMessage:{msg}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(email, pwd)
        connection.sendmail(email, email, email_message)


# Contact page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_data = request.form
        # print(user_data["name"])
        email_me(user_data["name"], user_data["email"], user_data["phone_number"], user_data["message"])
        return render_template('contact.html', heading=message, sub_heading=sub_msg)
    return render_template('contact.html', heading=contact_head, sub_heading=contact_sub)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
