from googlesearch import search
from utils import soupify


def wiki_summariser(question, index=0, num_lines=5):
    """Displays first 5 lines of a wikipedia page"""

    wiki_page = list(search(query=question, domains=['https://en.wikipedia.org/'], tld="com", num=10, stop=3, pause=1))

    soup = soupify(wiki_page[index])

    article = []
    for x in (soup.select('p')):
        article.append(x.text)

    result = ''.join(article[:num_lines])
    return print(result)


if __name__ == '__main__':
    wiki_summariser(question='napoleon')