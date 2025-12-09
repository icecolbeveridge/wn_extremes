import pandas as pd
import pyextremes
import matplotlib.pyplot as plt
import argparse

def get_extremes(filename,
    field="RAINFALL_M",
    threshold=10.0,
    return_period = [2, 5, 10, 25, 50, 100, 250, 500, 1000],
    alpha = 0.95,
    n_samples = 1000):

    series = pd.read_excel(
        filename,
        index_col = 0,
        parse_dates=True,
    ) # read in the excel file

    # We want the *start* of the hour rather than the end
    # Otherwise, it treats the last reading of the year as the first reading of the next year.
    series["DATE"] += pd.to_timedelta(series["HR"]-1, unit="h")

    # All we need is the field we're after (e.g. RAINFALL_M)
    # Sort it by date, drop any bad data, convert to a Series object
    clean = series[['DATE', field]].set_index('DATE').sort_index().dropna().squeeze()

    # pyextremes wraps a series in an EVA (extreme value analysis) object to provide helper functions.
    model = pyextremes.EVA(clean)

    # find all of the readings >= threshold, ignoring any other events within 24 hours of a peak.
    model.get_extremes("POT", threshold=threshold)

    # fit a generalised Pareto distribution (+ Poisson) to the extremes
    model.fit_model()

    summary = model.get_summary(
        return_period=return_period,
        alpha=alpha,
        n_samples=n_samples,
    )

    return model, summary


def show_data(model):
    # show all the data, with the peaks highlighted
    model.plot_extremes()
    plt.show()

def show_diagnostics(model, summary):
    print(summary)
    model.plot_diagnostic(alpha=alpha)
    plt.show()


filename = "data/Waddington_Station_Data.xlsx"
field = "RAINFALL_M"
threshold = 10.0
return_period=[2, 5, 10, 25, 50, 100, 250, 500, 1000]
alpha=0.95
n_samples=1000

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default=filename)
    parser.add_argument("-F", "--field", type=str, default=field)
    parser.add_argument("-t", "--threshold", type=float, default = threshold)
    parser.add_argument("-a", "--alpha", type=float, default=alpha)
    parser.add_argument("-n", "--n_samples", type=int, default=n_samples)
    args = parser.parse_args()

    model, summary = get_extremes(args.filename, args.field, args.threshold, return_period=return_period)

    # show_data(model)
    show_diagnostics(model, summary)
