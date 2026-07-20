import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from flask_mail import Mail, Message
import joblib
from groq import Groq
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'komalmore1742009@gmail.com'
app.config['MAIL_PASSWORD'] = ["rnit whmf ogdc vvun"]
load_dotenv()
mail = Mail(app)

client = Groq(api_key=os.getenv("kFHcMDi3E5tdSACduHEUWGdyb3FYPMliclQtbrhsobifGw85Qtw6"))

# Load trained model
model = joblib.load("model/disease_model.pkl")

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@app.route("/contact", 
           methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        try:
            # Email to Admin (You)
            admin_msg = Message(
                subject=f"New Contact: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=["komalmore1742009@gmail.com"]
            )

            admin_msg.body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

            mail.send(admin_msg)

            # Auto Reply to User
            user_msg = Message(
                subject="Thank You for Contacting Us",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            user_msg.body = f"""
Hello {name},

Thank you for contacting the Medical Disease Prediction System.

We have received your message successfully.
Our team will contact you soon.

Regards,
Medical Disease Prediction Team
"""

            mail.send(user_msg)

            return render_template("contact.html", success="Message sent successfully!")

        except Exception as e:
            return render_template("contact.html", success=f"Error: {e}")

    return render_template("contact.html")

# Prediction
@app.route("/predict", methods=["POST"])
def predict():
    fever = int(request.form["Fever"])
    cough = int(request.form["Cough"])
    headache = int(request.form["Headache"])
    fatigue = int(request.form["Fatigue"])

    prediction = model.predict([[fever, cough, headache, fatigue]])[0]

    return render_template(
        "result.html",
        prediction=f"Predicted Disease: {prediction}"
    )
@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are MediCare AI. Give simple, helpful medical information. Remind users to consult a doctor for diagnosis or treatment."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }

if __name__ == "__main__":
    app.run(debug=True)