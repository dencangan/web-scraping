from utils import EmailObject
from src.quotes import get_quote
from src.wiki_search import wiki_summariser
from datetime import datetime

day = datetime.today().strftime("%A")
date = datetime.today().strftime("%d %B %Y")

quote = get_quote(num_of_quotes=1)
wiki = wiki_summariser(randomise=True)

body = f"Quote of the day:<br><br>{quote} <br><br><br>Wikipedia article of the day:<br><br>{wiki}"

daily_email = EmailObject(email_text=body, add_css=True)
daily_email.send_email(to_address="dencan.gan@gmail.com", email_subject=day + ", " + date + ": Hang in there!")