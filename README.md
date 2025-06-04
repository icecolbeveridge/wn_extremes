# Estimated return periods of one-hour events

This script takes one-hour data from an Excel file formatted as:

  (src_id) (date) (hour) (rainfall)

and fits a generalised extreme value distribution to it.

The heavy lifting is done by the excellent [pyextremes package](https://georgebv.github.io/pyextremes/).

It outputs the value for return periods of 2, 5, 10, 25, 50, 100, 250, 500 and 1000 years, as well as the 95% confidence interval.

It also plots...
  * top-left: a return value plot, showing the model output and how the observations fit to it. The red line is the estimated value for a given return period, and the blue zone is the confidence interval). In a perfect world, the dots should lie on the red line.
  * top-right: a probability density plot. The observations are ticks on the x-axis, the blue bars are the binned counts, and the red line is the theoretical curve. Ideally, the blue bars line up with the red curve.
  * bottom-left: a [quantile-quantile plot](https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot). If two distributions match perfectly, the observation dots lie on the diagonal blue line.
  * bottom-right: a [probability-probability plot](https://en.wikipedia.org/wiki/P%E2%80%93P_plot)[^0]. If two distributions match perfectly, the observation dots lie on the diagonal blue line.

[^0]: The Q-Q plot plots the $k$th percentile of the observations against the $k$th percentile of the theoretical values -- so there's a point representing the median of each distribution, and a point representing the lower quartile, and a point representing the 93rd percentile, and so on. The P-P plot is a sort of inverse of that; for each observation, it plots its observed quantile as a function of its theoretical quantile. For example, the value of the observed median of the Waddington data is around the 43rd percentile of the fitted theoretical distribution.

## Usage


  `python extremes.py # runs with default values on Waddington data assumed to be in the data/ directory`

**Optional parameters (and defaults):**

*  `-f data/Waddington_Station_Data.xlsx # specify file to use`
*  `-F RAINFALL_M           # specify spreadsheet field name`
*  `-t 10.0                 # adjust the lower-bound threshold for the GEV`
*  `-a 0.95                 # width of confidence interval`
*  `-n 1000                 # number of samples for CI calculation`

[Picking the threshold value is more of an art than a science](https://georgebv.github.io/pyextremes/user-guide/5-threshold-selection/), and it's worth playing around with the parameter to find a good fit to the data.

For example, with the Waddington data, a 5mm threshold gives a better fit than the default 10mm threshold.
