from utils import EmailObject
from quotes import get_quote
from datetime import datetime

day = datetime.today().strftime("%A")
date = datetime.today().strftime("%d %B %Y")

quote = get_quote(num_of_quotes=1)

body = "Quote of the day: " + quote

daily_email = EmailObject(email_text=body, add_css=True)
daily_email.send_email(to_address="dencan.gan@gmail.com", email_subject=day + ", " + date + ": Hang in there!")