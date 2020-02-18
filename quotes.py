from utils import soupify
import random
from utils import EmailObject


def get_quote(num_of_quotes):

    random_page = random.randint(1, 100)
    quote_page = r"https://www.goodreads.com/quotes" + "?page=" + str(random_page)
    soup = soupify(quote_page)

    sep = "//"
    quotes_lst = []
    for x in (soup.find_all('div', class_='quoteText')):
        quote_with_author = x.text.replace("\n", "")
        clean = quote_with_author.split(sep, maxsplit=1)[0]
        quotes_lst.append(clean)

    if num_of_quotes > 1:
        for i in range(num_of_quotes):
            random_quote = random.randint(0, 29)
            quote = quotes_lst[random_quote]
            return quote

    else:
        random_quote_idx = random.randint(0, 29)
        return quotes_lst[random_quote_idx]


if __name__ == "__main__":
    get_quote(num_of_quotes=1)

    email = EmailObject(email_text="hi this is a test email", add_css=True)
    email.send_email(to_address="dencan.gan@gmail.com", email_subject="test email")