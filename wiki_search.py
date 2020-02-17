from googlesearch import search
from utils import soupify


def wiki_summariser(search_term, num_lines=5):
    """Displays first 5 lines of a wikipedia page

    Args:
        search_term (str): Key word to search.
        num_lines (int): Number of lines to display.

    Returns:
        Prints output.
    """

    wiki_page = list(search(query=search_term, domains=['https://en.wikipedia.org/'], tld="com", num=10, stop=3, pause=1))

    soup = soupify(wiki_page[0])

    article = []
    for x in (soup.select('p')):
        article.append(x.text)

    result = ''.join(article[:num_lines])
    return print(result)


if __name__ == '__main__':
    wiki_summariser(search_term='blanket')