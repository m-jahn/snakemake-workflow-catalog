import json
import pandas as pd
import altair as alt
from datetime import datetime


def bar_chart(df, metric, title, colors):
    custom_scale = alt.Scale(domain=df[metric].values, range=colors)
    chart = alt.Chart(
        df,
        title=alt.Title(title, anchor="start", orient="top", offset=10, frame="group"),
    ).encode(
        x=alt.X("count:Q", title="Frequency").axis(None),
        y=alt.Y(f"{metric}:N", title=metric, sort=df[metric].values).axis(
            title="",
            ticks=False,
            grid=False,
            labelLimit=60,
            maxExtent=80,
            minExtent=80,
            labelAlign="right",
        ),
        text="count",
        tooltip=[metric, "count"],
        color=alt.Color(f"{metric}:N", scale=custom_scale, legend=None),
    )
    chart = chart.mark_bar() + chart.mark_text(align="left", dx=2)
    chart.configure_view(stroke=None).properties(width="container", height=120).save(
        f"_static/chart_{metric}.html", embed_options={"actions": False}
    )


def build_wf_charts():

    # import workflow data as table
    df = pd.read_json("../data.json")

    # import topics stats and transform to table
    with open("_static/topics_stats.json", "r") as f:
        topics = json.load(f)
    topics = [value for key, value in topics.items()]
    df_topics = pd.DataFrame(topics)

    # define, register and enable theme
    @alt.theme.register("transparent", enable=True)
    def transparent() -> alt.theme.ThemeConfig:
        return {
            "usermeta": {"embedOptions": {"theme": "quartz"}},
            "config": {
                "title": {"fontSize": 12, "color": "grey"},
                "background": "transparent",
            },
        }

    # define a custom color scale
    colors = ["#58e3b5", "#10b981", "#059669", "#06865e", "#056d4c", "#0a4d37"]

    # PLOT 1: bar chart for standardized vs other workflows
    df_standard = df["standardized"].value_counts().reset_index()
    df_standard["standardized"] = df_standard["standardized"].apply(
        lambda x: "standardized" if x else "other"
    )
    bar_chart(df_standard, "standardized", "Number of workflows", colors)

    # PLOT 2: recently changed workflows
    df["age"] = df["updated_at"].apply(lambda x: (datetime.today() - x).days)
    bins = [0, 1, 7, 31, 365]
    labels = ["yesterday", "last week", "last month", "last_year"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)
    df_age = df["age_group"].value_counts().reset_index()
    bar_chart(df_age, "age_group", "Recently updated workflows", colors)

    # PLOT 3: stargazer counts
    df_stars = (
        pd.cut(
            df["stargazers_count"],
            bins=[-1, 0, 5, 10, 20, 50, 10000],
            labels=["0", "1-5", "6-10", "11-20", "21-50", ">50"],
        )
        .value_counts()
        .reset_index()
        .sort_values(by="stargazers_count")
    )
    bar_chart(df_stars, "stargazers_count", "Workflows by stars", colors)

    # PLOT 4: subscriber counts
    df_subscribers = (
        pd.cut(
            df["subscribers_count"],
            bins=[-1, 0, 5, 10, 20, 50, 10000],
            labels=["0", "1-5", "6-10", "11-20", "21-50", ">50"],
        )
        .value_counts()
        .reset_index()
        .sort_values(by="subscribers_count")
    )
    bar_chart(df_subscribers, "subscribers_count", "Workflows by Watchers", colors)

    # PLOT 5: Workflows by linting and formatting status (Null == passed)
    def eval_status(ls):
        if all(pd.isnull(ls)):
            return "All passed"
        elif pd.isnull(ls.iloc[0]) and not pd.isnull(ls.iloc[1]):
            return "Formatting failed"
        elif pd.isnull(ls.iloc[1]) and not pd.isnull(ls.iloc[0]):
            return "Linting failed"
        else:
            return "All failed"

    df_health = (
        df[["linting", "formatting"]]
        .apply(lambda row: eval_status(row), axis=1)
        .value_counts()
        .reset_index()
        .rename(columns={"index": "health"})
    )
    bar_chart(df_health, "health", "Workflows by Linting & Formatting", colors)

    # PLOT 6: workflows by topic
    df_topics = (
        df_topics.rename(columns={"number": "count", "name": "topic"})
        .sort_values(by="count", ascending=False)
        .iloc[:6]
    )
    bar_chart(df_topics, "topic", "Workflows by Topic", colors)

    # closing statement
    print("Charts rendered successfully.")
    return None
