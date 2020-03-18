from utils import EmailObject
from src.quotes import get_quote
from src.wiki_search import wiki_summariser
from datetime import datetime
from src.covid19.corona import summary

day = datetime.today().strftime("%A")
date = datetime.today().strftime("%d %B %Y")


def morning_email():

    quote = get_quote(num_of_quotes=1)
    wiki = wiki_summariser(randomise=True)

    body = f"Quote of the day:<br><br>{quote} <br><br><br>Wikipedia article of the day:<br><br>{wiki}"

    daily_email = EmailObject(email_text=body, add_css=True)
    daily_email.send_email(to_address="dencan.gan@gmail.com", email_subject=day + ", " + date + ": Hang in there!")


def cov19_email():

    ytd_cases, tower_hamlets, london = summary()

    covid19_email = EmailObject(email_text="COVID19 update: ", add_css=True,
                                email_table=[ytd_cases, london, tower_hamlets])

    covid19_email.send_email(to_address="dencan.gan@gmail.com", email_subject=day + ", " + date + ": COVID19 update")


if __name__ == "__main__":
    cov19_email()
