import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        df.index,
        df["value"]
    )

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    df_bar = (
        df_bar
        .groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    df_bar = df_bar[months]

    # Draw bar plot
    fig = df_bar.plot(
        kind="bar",
        figsize=(12, 6)
    )

    fig.set_xlabel("Years")
    fig.set_ylabel("Average Page Views")

    fig.legend(
        title="Months"
    )

    # Save image and return fig
    fig.figure.savefig("bar_plot.png")
    return fig.figure


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box["year"] = [
        d.year for d in df_box.date
    ]

    df_box["month"] = [
        d.strftime("%b")
        for d in df_box.date
    ]

    # Draw box plots
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(15, 5)
    )

    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title(
        "Year-wise Box Plot (Trend)"
    )

    axes[0].set_xlabel(
        "Year"
    )

    axes[0].set_ylabel(
        "Page Views"
    )


    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title(
        "Month-wise Box Plot (Seasonality)"
    )

    axes[1].set_xlabel(
        "Month"
    )

    axes[1].set_ylabel(
        "Page Views"
    )

    # Save image and return fig
    fig.savefig("box_plot.png")
    return fig