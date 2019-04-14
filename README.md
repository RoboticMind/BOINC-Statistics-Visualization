# BOINC-Statistics-Visualization
Interactive visual for viewing total BOINC credits

### Webpage Information
Informational & interactive chart site is on the [gh-pages branch](https://github.com/RoboticMind/BOINC-Statistics-Visualization/tree/gh-pages)

### Python Code Information
Python 3, [bokeh](https://bokeh.pydata.org), and the Stats.csv file is required to run plot_generator.py. When run,
it will generate an HTML file containing the interactive chart. This file will automatically be displayed after running. If
you have issues in viewing the chart, try changing the render mode from webgl to canvas in the line ```output_backend='webgl'```.

For data_extrapolator.py: Python 3 and the Stats.csv file are required to run. If you want to sort newly appended data change ```writeolddata=False``` to
```writeolddata=True```. If you want to generate extrapolated points from the Credit per day column, change ```extractnew=False``` to
```extractnew=True```. 

### If Things Don't Work

Check for [an issue](https://github.com/RoboticMind/BOINC-Statistics-Visualization/issues) and if it doesn't exist, [open one.](https://github.com/RoboticMind/BOINC-Statistics-Visualization/issues/new)
Please be as specific as possible in your description of the problem. Include things like the version of Python you are running. 
