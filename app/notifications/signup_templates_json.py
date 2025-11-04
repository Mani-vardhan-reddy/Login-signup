signup_templates = [
    {
        "notifiation_slug": "welcome_email",
        "notification_name": "Welcome Email to User",
        "subject":"Hi {{user_name}} Welcome to the App",
        "content": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/><title>Welcome Email</title><style>body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background-color:#f4f6f8;color:#333;margin:0;padding:0}.email-container{max-width:600px;background:#fff;margin:40px auto;border-top:6px solid #4a90e2;border-bottom:6px solid #4a90e2;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden}.header{text-align:center;padding:20px;background-color:#f9fafb;border-bottom:1px solid #e5e7eb}.header h1{font-size:24px;color:#4a90e2;margin:0}.content{padding:30px;line-height:1.6;font-size:16px}.content p{margin-bottom:20px}.footer{text-align:center;background-color:#f9fafb;padding:15px;font-size:14px;color:#666;border-top:1px solid #e5e7eb}.footer a{color:#4a90e2;text-decoration:none;font-weight:500}</style></head><body><div class="email-container"><div class="header"><h1>{{ product_name }}</h1></div><div class="content"><p>Hi <strong>{{ user_name }}</strong>,</p><p>Welcome onboard! We are thrilled to have you with us.</p><p>Please feel free to contact our support team for any further queries:<br/>📞 <strong>{{ mobile_number }}</strong><br/>📧 <strong>{{ email }}</strong></p><p>Best Regards,<br/><strong>{{ product_name }} Team</strong></p></div><div class="footer"><p>© {{ product_name }} | All rights reserved.</p></div></div></body></html>""",
        "variables": [
            "user_name",
            "product_name",
            "mobile_number",
            "email"
        ],
        "notification_type":"email"
    },
    {
      "notifiation_slug": "mobile_otp_email",
        "notification_name": "Mobile OTP Verification",
        "subject":"Hi {{user_name}} Verify your Mobile Number",
        "content": """"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'/><meta name='viewport' content='width=device-width, initial-scale=1.0'/><title>Welcome Email</title><style>body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background-color:#f4f6f8;color:#333;margin:0;padding:0}.email-container{max-width:600px;background:#fff;margin:40px auto;border-top:6px solid #4a90e2;border-bottom:6px solid #4a90e2;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden}.header{text-align:center;padding:20px;background-color:#f9fafb;border-bottom:1px solid #e5e7eb}.header h1{font-size:24px;color:#4a90e2;margin:0}.content{padding:30px;line-height:1.6;font-size:16px}.content p{margin-bottom:20px}.footer{text-align:center;background-color:#f9fafb;padding:15px;font-size:14px;color:#666;border-top:1px solid #e5e7eb}.footer a{color:#4a90e2;text-decoration:none;font-weight:500}</style></head><body><div class='email-container'><div class='header'><h1>{{ product_name }}</h1></div><div class='content'><p>Hi <strong>{{ user_name }}</strong>,</p><p>Your one time password for mobile number verification is.</p><p>OTP: {{ otp }}</p><p>Please feel free to contact our support team for any further queries:<br/>📞 <strong>{{ mobile_number }}</strong><br/>📧 <strong>{{ email }}</strong></p><p>Best Regards,<br/><strong>{{ product_name }} Team</strong></p></div><div class='footer'><p>© {{ product_name }} | All rights reserved.</p></div></div></body></html>""",
        "variables": [
            "user_name",
            "product_name",
            "otp",
            "mobile_number",
            "email"
        ],
        "notification_type":"email"  
    },
    {
       "notifiation_slug": "emailverification_email",
        "notification_name": "Email Verification",
        "subject":"Hi {{user_name}} Verify your Email",
        "content": """<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'/><meta name='viewport' content='width=device-width, initial-scale=1.0'/><title>Welcome Email</title><style>body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background-color:#f4f6f8;color:#333;margin:0;padding:0}.email-container{max-width:600px;background:#fff;margin:40px auto;border-top:6px solid #4a90e2;border-bottom:6px solid #4a90e2;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden}.header{text-align:center;padding:20px;background-color:#f9fafb;border-bottom:1px solid #e5e7eb}.header h1{font-size:24px;color:#4a90e2;margin:0}.content{padding:30px;line-height:1.6;font-size:16px}.content p{margin-bottom:20px}.footer{text-align:center;background-color:#f9fafb;padding:15px;font-size:14px;color:#666;border-top:1px solid #e5e7eb}.footer a{color:#4a90e2;text-decoration:none;font-weight:500}</style></head><body><div class='email-container'><div class='header'><h1>{{product_name}}</h1></div><div class='content'><p>Hi <strong>{{user_name}}</strong>,</p><p>To verify your email please click on the link below.</p><p>link: {{verify_link}}</p><p>Please feel free to contact our support team for any further queries:<br/>📞 <strong>{{mobile_number}}</strong><br/>📧 <strong>{{email}}</strong></p><p>Best Regards,<br/><strong>{{product_name}} Team</strong></p></div><div class='footer'><p>© {{product_name}} | All rights reserved.</p></div></div></body></html>""",
        "variables": [
            "user_name",
            "product_name",
            "verify_link",
            "mobile_number",
            "email"
        ],
        "notification_type":"email"  
    }
]