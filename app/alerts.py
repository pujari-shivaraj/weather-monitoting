from app.database import MongoDBClient
from app.schemas.weather import AlertData
import smtplib
from email.mime.text import MIMEText
from app.config import Config
from datetime import datetime

mongodb_client = MongoDBClient()

def send_email_alert(alert: AlertData):
    """Send an email alert when the threshold is breached."""
    msg = MIMEText(alert.alert_message)
    msg["Subject"] = f"Weather Alert for {alert.city}"
    msg["From"] = "your_email@example.com"  # Replace with your email
    msg["To"] = "recipient_email@example.com"  # Replace with recipient email

    with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server
        server.starttls()
        server.login("your_email@example.com", "your_password")  # Use your email login
        server.sendmail(msg["From"], msg["To"], msg.as_string())

def check_alerts(weather_data):
    """Check if the latest weather data breaches any thresholds."""
    for city, data in weather_data.items():
        if data["temp_value"] > Config.ALERT_THRESHOLD_TEMP:
            alert = AlertData(
                city=city,
                triggered_at=datetime.now(),
                alert_type="temperature",
                alert_message=f"Temperature exceeded {Config.ALERT_THRESHOLD_TEMP}°C.",
                current_value=data["temp_value"],
                threshold_value=Config.ALERT_THRESHOLD_TEMP
            )
            send_email_alert(alert)
            # Store alert in the database if necessary
