import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# SMTP Configuration - Replace with your actual credentials
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@yourcompany.com")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Reminder System")


def send_reminder_notification(reminder_data: dict) -> bool:
    """
    Send reminder notification via email.
    
    Args:
        reminder_data: Dictionary containing:
            - entity_type: Type of entity (e.g., 'interviewer')
            - entity_id: ID of the entity
            - event_type: Type of event (e.g., 'feedback_form')
            - channel: Notification channel (should be 'email')
            - recipient_email: Email address to send to
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # For demo purposes, just log the action
    # In production, replace this with actual SMTP sending
    
    try:
        recipient = reminder_data.get('recipient_email', 'recipient@example.com')
        entity_type = reminder_data.get('entity_type', 'Unknown')
        entity_id = reminder_data.get('entity_id', 'Unknown')
        event_type = reminder_data.get('event_type', 'Unknown')
        
        # Create email message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"Reminder: {event_type.replace('_', ' ').title()}"
        message['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        message['To'] = recipient
        
        # Email body
        text_body = f"""
Hello,

This is a reminder regarding: {event_type.replace('_', ' ').title()}

Entity Type: {entity_type}
Entity ID: {entity_id}

Please take the necessary action.

Best regards,
Reminder System
"""
        
        html_body = f"""
<html>
  <body>
    <p>Hello,</p>
    <p>This is a reminder regarding: <strong>{event_type.replace('_', ' ').title()}</strong></p>
    <ul>
      <li><strong>Entity Type:</strong> {entity_type}</li>
      <li><strong>Entity ID:</strong> {entity_id}</li>
    </ul>
    <p>Please take the necessary action.</p>
    <p>Best regards,<br>Reminder System</p>
  </body>
</html>
"""
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        message.attach(part1)
        message.attach(part2)
        
        # For demo/testing: Just print the email
        print(f"📧 [DEMO MODE] Email notification:")
        print(f"   To: {recipient}")
        print(f"   Subject: {message['Subject']}")
        print(f"   Body: {text_body[:100]}...")
        
        # Uncomment below to actually send emails
        # Make sure to set proper SMTP credentials in .env file
        
        # with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        #     server.starttls()
        #     server.login(SMTP_USERNAME, SMTP_PASSWORD)
        #     server.send_message(message)
        #     print(f"✅ Email sent successfully to {recipient}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email notification: {e}")
        return False


def send_slack_notification(reminder_data: dict) -> bool:
    """
    Placeholder for Slack notifications.
    Implement using slack_sdk or webhook URLs.
    """
    print(f"📱 [DEMO MODE] Slack notification: {reminder_data}")
    return True


def send_sms_notification(reminder_data: dict) -> bool:
    """
    Placeholder for SMS notifications.
    Implement using Twilio or similar service.
    """
    print(f"📲 [DEMO MODE] SMS notification: {reminder_data}")
    return True


def trigger_notification(reminder_data: dict) -> bool:
    """
    Route notification to appropriate channel.
    
    Args:
        reminder_data: Dictionary with channel and notification details
        
    Returns:
        bool: Success status
    """
    channel = reminder_data.get('channel', 'email')
    
    if channel == 'email':
        return send_reminder_notification(reminder_data)
    elif channel == 'slack':
        return send_slack_notification(reminder_data)
    elif channel == 'sms':
        return send_sms_notification(reminder_data)
    else:
        print(f"⚠️ Unknown notification channel: {channel}")
        return False