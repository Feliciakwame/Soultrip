from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

email_bp=Blueprint('email', __name__)

@email_bp.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    contacts=data.get('contacts',[])
    latitude=data.get('latitude')
    longitude=data.get('longitude')
    
    if not contacts or not latitude or not longitude:
        return jsonify({'error': 'Missing data'}), 400
    
    map_link=f"https://maps.google.com/?q={latitude},{longitude}"
    subject="📍 Live Location from SoulTrip"
    body=f"Here's the current location of your loved one:\n{map_link}"
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            for contact in contacts:
                msg=MIMEText(body)
                msg['Subject']=subject
                msg['From']=EMAIL_ADDRESS
                msg['To']=contact
                smtp.send_message(msg)  
                
        return jsonify ({'message':'Location sent via email!'}), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500