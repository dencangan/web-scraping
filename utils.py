"""
Initial webscraping functions.
GET request and BeautifulSoup parsing.
"""

from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd


def soupify(url):
    """Attempts to get the content at `url` by making an HTTP GET request. Then uses BeautifulSoup to parse the html.

    Arg:
        url: str
            Link to url to scrape information
        parser: str
            Bs4 parser type, see documentation for parser types. Defaults to 'html.parser'.
            https://www.crummy.com/software/BeautifulSoup/bs4/doc/
            
    Returns:
    If parsed html content, otherwise return None.
    
    The closing() function ensures that any network resources are freed when they go out of scope in that with block.
    Using closing() like that is good practice and helps to prevent fatal errors and network timeouts.
    """

    try:
        # Sending GET
        with closing(get(url, stream=True)) as resp:
            if check_response(resp):
                content = resp.content
                print('Successfully received {u}'.format(u=url))

                # Using BeautifulSoup to parse
                bs4_parse = BeautifulSoup(content, features="lxml")
                return bs4_parse

            else:
                print('Failed to receive {u}'.format(u=url))
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def check_response(resp):
    """Checks if the response is correct. Returns True if the response seems to be HTML, False otherwise.
    """
    # 'text/html;charset=utf-8' should be expected
    content_type = resp.headers['Content-Type'].lower()

    # Status_code == 200 means http status is OK
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > -1


def char_to_date(s, dayfirst=False, format=None, infer_datetime_format=False):
    """Turning date from object to np.datetime64

    Parameters
    ----------
        s : pd.Dataframe, pd.Series
            Pass in dataframe if multi column process is needed
    Returns
    -------
        pd.Series
        pd.DataFrame
            all columns containing "date" (case in-sensitive) will be amended
    Note
    -----
        This method can handle EITHER "/" or "-" date separators but not a combination of both.
        Users should check that there are no mixtures of separators if s is an array
    """

    def find_format(s):
        year_pattern = "%Y"

        try:
            sep = "/"
            if pd.Series(s).str.contains("-").all():
                sep = "-"
            x = pd.Series(s).str.split("/|-", expand=True).values
            x = x.astype(int)
            month_pattern = "%m"
        except ValueError:
            month_pattern = "%b"

        year_col, month_col, date_col = None, None, None

        for i in range(x.shape[-1]):
            if x[:, i].dtype != object:
                if all(x[:, i].astype(int) > 1000):
                    year_col = i
                elif all(x[:, i].astype(int) <= 12):
                    month_col = i
                elif all(x[:, i].astype(int) <= 31):
                    date_col = i
            else:
                date_col, month_col, year_col = 0, 1, 2  # only month can be string and must be in the middle
                break

        assert year_col is not None, "Cannot find year in date string"

        try:
            year_pattern = "%Y" if (x[:, year_col].astype(int) > 1000).all() else "%y"
        except (ValueError, TypeError, IndexError):
            return None  # last resort couldn"t figure format out, let pandas do it

        month_and_date = lambda m, d, month_pattern: sep.join(("%d", "%s" % month_pattern)) if m > d else sep.join(
            ("%s" % month_pattern, "%d"))

        if year_col == 0:
            if month_col is not None and date_col is not None:
                fmt = sep.join((year_pattern, month_and_date(month_col, date_col, month_pattern)))
            else:
                fmt = sep.join((year_pattern, "%s" % month_pattern, "%d"))  # default to non US style
        elif year_col == 2:
            if month_col is not None and date_col is not None:
                fmt = sep.join((month_and_date(month_col, date_col, month_pattern), year_pattern))
            else:
                fmt = sep.join(("%d", "%s" % month_pattern, year_pattern))  # default to non US style
        else:
            raise ValueError("year in the middle of date separators!")

        return fmt

    # This is an extremely fast approach to datetime parsing. Some dates are often repeated. Rather than
    # re-parse these, we store all unique dates, parse them, and use a lookup to convert all dates.
    if isinstance(s, pd.DataFrame):
        out = s.copy(True)  # this is the bottleneck
        for columnName, column in out.iteritems():
            # loop through all the columns passed in
            if "date" in columnName.lower():
                if column.dtype != "<M8[ns]" and ~column.isnull().all():
                    # if date is provided as a string then ignore and set to int
                    try:
                        col = column.astype(int)
                        out[columnName] = col
                    except:
                        # find the date columns(case in-sensitive), if pandas cant find the format,
                        # ignore error and maintain input
                        uDates = pd.to_datetime(column.unique(), format=find_format(column.unique()), errors="ignore")
                        dates = dict(zip(column.unique(), uDates.tolist()))
                        out[columnName] = column.map(dates.get)

        return out

    else:
        if s.dtype == "<M8[ns]":
            return s
        uDates = pd.to_datetime(s.unique(), format=find_format(s.unique()))
        dates = dict(zip(s.unique(), uDates.tolist()))

        return s.map(dates.get)

