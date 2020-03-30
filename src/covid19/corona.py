from arctic import Arctic
import json
import seaborn as sns
from matplotlib import pyplot as plt

mongo_credentials = json.load(open(r"C:\Users\Dencan Gan\Credentials\credentials.json"))["mongodb"]

# Connect to arctic library
a = Arctic(f"mongodb+srv://{mongo_credentials['username']}:{mongo_credentials['password']}@personaldatabase-rgdhs.azure.mongodb.net/test?retryWrites=true&w=majority")
covid19_lib = a["covid19"]

df_daily = covid19_lib.read("daily_cases").data
df_county = covid19_lib.read("country_cases").data
df_nhsr = covid19_lib.read("nhsr_cases").data


def format_data(daily_lookback):

    # Uploaded data
    cases_yesterday = df_daily.tail(daily_lookback).reset_index().drop(columns=["index"])
    cases_yesterday = cases_yesterday.rename(columns={"DateVal": "Date", "CMODateCount": "Daily Cases", "CumCases":
        "Total Cases"})
    cases_yesterday["Country"] = "United Kingdom"
    cases_yesterday = cases_yesterday[["Date", "Country", "Daily Cases", "Total Cases"]]

    tower_hamlets = df_county[df_county["GSS_NM"].isin(["Tower Hamlets"])].reset_index().drop(columns=["index", "GSS_CD"])
    tower_hamlets = tower_hamlets.rename(columns={"GSS_NM": "Area", "TotalCases": "Total Cases"})

    london = df_nhsr[df_nhsr["NHSRNm"].isin(["London"])].reset_index().drop(columns=["index", "GSS_CD"])
    london = london.rename(columns={"NHSRNm": "City", "TotalCases": "Total Cases"})

    return cases_yesterday, tower_hamlets, london


def visualise():
    sns.lineplot(data=df_daily, x="DateVal", y="CumCases")
    sns.barplot(data=df_nhsr, x="NHSRNm", y="TotalCases")
    plt.show()


if __name__ == "__main__":
    daily, county, city = format_data(daily_lookback=2)
