import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

API_URL = "http://127.0.0.1:5001/api/recommend/"

users = [{"user_id": 196, "email": "ramazan202378@gmail.com"}]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "ramazabqayev@gmail.com"
EMAIL_PASSWORD = "dywn acal rvem ojsq"

def get_recommendations(user_id):
    try:
        response = requests.get(f"{API_URL}{user_id}")
        response.raise_for_status()
        return response.json().get("recommendations", [])
    except requests.exceptions.RequestException as e:
        print(f"API hatası (user_id={user_id}): {e}")
        return []

def send_email(to_email, recommendations):
    if not recommendations:
        print(f"{to_email} için öneri bulunamadı.")
        return

    # HTML formatında e-posta oluştur
    html_content = "<h2>Haftalık Film Önerileriniz</h2><ul>"
    for movie in recommendations:
        html_content += f'<li><a href="{movie["url"]}">{movie["title"]}</a></li>'
    html_content += "</ul>"

    # MIME yapısı
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Haftalık Film Önerileriniz"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    # SMTP ile gönder
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"E-posta gönderildi: {to_email}")
    except Exception as e:
        print(f"E-posta gönderilemedi ({to_email}): {e}")

def run_weekly_campaign():
    print("Haftalık E-posta Kampanyası Başlatılıyor...\n")
    for user in users:
        recommendations = get_recommendations(user["user_id"])
        send_email(user["email"], recommendations)
    print("\nHaftalık E-posta Kampanyası Tamamlandı!")

# -----------------------
# Çalıştırma
# -----------------------
if __name__ == "__main__":
    run_weekly_campaign()
