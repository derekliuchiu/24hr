import smtplib
import ssl
import json
import os

def texter(name, works):
    with open("price.txt", "r") as f:
        price_dict = json.loads(f.readline())
    price = price_dict[name]

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    sender_email = os.getenv("gym_Sender")
    receiver_email = os.getenv("gym_receiver")
    password = os.getenv("gym_password")
    
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # check connection
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # check connection
        server.login(sender_email, password)

        # Send email here
        if not works:
            server.sendmail(sender_email, receiver_email, f"Scraper not working for {name} location, check xPath.")
        else:
            server.sendmail(sender_email, receiver_email, f"Price for {name} location now ${price}.")

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
