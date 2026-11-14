"""
=============================================================================
TRAVELO - REAL SMTP EMAIL TEST SCRIPT
=============================================================================
Run this script to verify your Gmail / SMTP configuration:
    python test_smtp.py

It will test your connection to smtp.gmail.com and send a live test OTP email.
=============================================================================
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Reconfigure console output for Windows UTF-8 safety
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelo_project.settings')

def run_smtp_test():
    print("=" * 65)
    print("   TRAVELO - REAL SMTP EMAIL CONNECTION TEST")
    print("=" * 65)

    from travelo_app.otp_config import (
        EMAIL_HOST,
        EMAIL_PORT,
        EMAIL_USE_TLS,
        EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD,
        DEFAULT_FROM_EMAIL
    )

    print(f"\n[+] Configured Host: {EMAIL_HOST}:{EMAIL_PORT}")
    print(f"[+] Sender Email:   {EMAIL_HOST_USER}")
    
    masked_pw = ("*" * len(EMAIL_HOST_PASSWORD)) if EMAIL_HOST_PASSWORD else "[NOT SET]"
    print(f"[+] App Password:   {masked_pw}")

    if not EMAIL_HOST_PASSWORD:
        print("\n[!] NOTICE: EMAIL_HOST_PASSWORD is currently empty in travelo_app/otp_config.py.")
        print("\nTo connect your real Gmail:")
        print("  1. Go to https://myaccount.google.com/apppasswords")
        print("  2. Create an App Password for 'Travelo Website'")
        print("  3. Copy the 16-character code (e.g. 'abcd efgh ijkl mnop')")
        print("  4. Open travelo_app/otp_config.py and set:")
        print("     EMAIL_HOST_USER = 'your_actual_gmail@gmail.com'")
        print("     EMAIL_HOST_PASSWORD = 'your_16_character_code'")
        print("  5. Re-run: python test_smtp.py\n")
        return

    test_recipient = input(f"\nEnter recipient email to receive test OTP (press Enter to send to {EMAIL_HOST_USER}): ").strip()
    if not test_recipient:
        test_recipient = EMAIL_HOST_USER

    print(f"\n[>] Connecting to {EMAIL_HOST}:{EMAIL_PORT} with TLS...")
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=15)
        server.set_debuglevel(0)
        if EMAIL_USE_TLS:
            server.starttls()
            print("[+] TLS encryption established.")

        print(f"[>] Authenticating as {EMAIL_HOST_USER}...")
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD.replace(" ", ""))
        print("[+] Authentication SUCCESSFUL!")

        # Compose test email
        otp_code = "789123"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Travelo Verification Code: {otp_code} (Test Email)"
        msg["From"] = DEFAULT_FROM_EMAIL
        msg["To"] = test_recipient

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #f8fafc; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: white; border-radius: 10px; border: 1px solid #e2e8f0; padding: 24px; text-align: center;">
                <h2 style="color: #0f172a; margin-top: 0;">Travel<span style="color: #f59e0b;">o</span> OTP Verification</h2>
                <p style="color: #64748b;">Your SMTP integration is working successfully!</p>
                <div style="background: #fffbeb; border: 2px dashed #f59e0b; border-radius: 8px; padding: 12px; margin: 20px 0; font-size: 28px; font-weight: bold; letter-spacing: 6px; color: #b45309;">
                    {otp_code}
                </div>
                <p style="font-size: 13px; color: #94a3b8;">This is a live test email sent via Python SMTP directly to your inbox.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        print(f"[>] Sending live test OTP to {test_recipient}...")
        server.sendmail(EMAIL_HOST_USER, [test_recipient], msg.as_string())
        server.quit()

        print("\n" + "=" * 65)
        print("🎉 SUCCESS! Real email sent successfully!")
        print(f"Check the inbox (and spam/promotions folder) of: {test_recipient}")
        print("Your Travelo website will now send real OTPs to every customer!")
        print("=" * 65 + "\n")

    except smtplib.SMTPAuthenticationError as auth_err:
        print("\n" + "!" * 65)
        print("❌ AUTHENTICATION ERROR:")
        print(f"Details: {auth_err}")
        print("\nWhy this happens with Gmail:")
        print("1. Google requires a 16-character 'App Password', not your regular login password.")
        print("2. You must have 2-Step Verification turned ON in your Google Account.")
        print("3. Generate your 16-character code here: https://myaccount.google.com/apppasswords")
        print("4. Paste that 16-character password into travelo_app/otp_config.py")
        print("!" * 65 + "\n")
    except Exception as e:
        print(f"\n❌ FAILED TO SEND EMAIL: {e}\n")

if __name__ == '__main__':
    run_smtp_test()
