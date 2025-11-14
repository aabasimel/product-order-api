from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
import jwt
from datetime import datetime, timedelta
from django.conf import settings
logger = logging.Logger(__name__)

@shared_task
def send_order_confirmation_email(order_id, user_email, user_name=None):
    try:
        subject = f"Order Confirmation - #{order_id}"
        
        # Personalized message
        greeting = f"Hi {user_name}," if user_name else "Hello,"
        
        message = f"""
        {greeting}

        We're writing to confirm that your order has been successfully placed!

        Order Details:
        - Order ID: #{order_id}
        - Account: {user_email}
        
        You'll receive another email when your order ships.

        If you have any questions about your order, please reply to this email.

        Thank you for choosing us!

        Warm regards,
        The Team at Your Company
        """
        
        send_mail(
            subject=subject,
            message=message.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        return f"Email sent to {user_email}"
        
    except Exception as e:
        logger.error(f"Failed to send email for order {order_id}: {str(e)}")
        return f"Error: {str(e)}"
    
@shared_task
def send_verification_email(email,link):
    try:
        subject = "Email Verification"
        message = f"Please verify your email by clicking on the following link: {link}"
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return f"Verification email sent to {email}"
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {str(e)}")
        return f"Error: {str(e)}"