import csv
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Tabs, Panel, DateSlider, Toggle
from bokeh.layouts import layout
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, LabelSet
dates=[]
stats=[]
with open('Stats.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	csvreader = list(csvreader)[1:] #[1:] drops headers
	for rawrow in csvreader:
		rowdata=rawrow[0].split(',')
		date=rowdata[0].split('-')
		date=datetime.date(int(date[0]),int(date[1]),int(date[2]))
		dates.append(date)
		stats.append(int(float(rowdata[1])))

output_file('BOINC Total Credit Over Time.html', title='BOINC Total Credit Over Time')

dispsource=ColumnDataSource(data=dict(x=dates,
                                  y=stats))

eventdates=[datetime.date(2004,6,22),datetime.date(2014,3,8),datetime.date(2017,6,14)]
labeltext=['Seti@home starts to use BOINC','Bitcoin Utopia Begins','Bitcoin Utopia Ends']
eventstats=[]
for date in eventdates:
    closestdate=min(dates, key=lambda x:abs(x-date)) #find the closest date in dates
    closestdate=dates.index(closestdate) #change from date to the index
    eventstats.append(stats[closestdate]) #adds stats at the closest date
labelsource=ColumnDataSource(data=dict(x=eventdates,y=eventstats,text=labeltext))

panels=[]
plots=[]
for axistype in ['linear','log']:
    labels = LabelSet(x='x',
                      y='y',
                      text='text',
                      source=labelsource,
                      angle=-3.14/2) #-pi/2 is 90 deg clockwise (makes it virtical)
    p = figure(plot_width=650, 
               plot_height=600,
               x_axis_type='datetime',
               y_axis_type=axistype,
               x_axis_label='Date',
               y_axis_label='Total Credit',
               x_range=(min(dates),max(dates)),
               output_backend='webgl')
    p.add_layout(labels) #add annoations to the charts
    try:
        p.left[0].formatter.use_scientific = False #disable scientific notation
    except:
        pass #fails if using log scale so it's ignore if failed
    p.title.text = 'BOINC Total Credit Over Time'
    p.title.align = 'center'
    p.add_tools(HoverTool(tooltips = [
            ('Date','@x{%F}'), # {%F} formats dates like YYYY-MM-DD 
            ('Total Credit','@y')],
            formatters={'x': 'datetime'}))
    p.scatter('x','y',source=dispsource, size=2, color='navy', alpha=0.5)
    plots.append(p)
    panels.append(Panel(child=p,title=axistype))

tabs=Tabs(tabs=panels)

callback= CustomJS(args=dict(stats=stats,dates=dates,plots=plots), code='''
    var len = cb_obj.value;
    var closest = stats[dates.indexOf(dates.reduce(function(prev, curr) {
        return (Math.abs(curr - len) < Math.abs(prev - len) ? curr : prev);
    }))]
    plots[0].x_range.end=len;
    plots[0].y_range.end=closest;
    plots[0].y_range.start=0;
    plots[1].x_range.end=len;
    plots[1].y_range.end=closest;
    plots[1].y_range.start=1;
''')
#changes x range to be (0,slider_value)
#changes y range to be (0 or 1, the closest stastics value to slider)

slider = DateSlider(start=min(dates), end=max(dates), value=max(dates), step=1, title='Time')
slider.js_on_change('value', callback)


loopchange = CustomJS(args=dict(slider=slider,endlen=max(dates),minlen=min(dates)), code='''
    function sleep(ms) {
       return new Promise(resolve => setTimeout(resolve, ms));
    }
    async function run() {
        var len = slider.value;
        var loopcount=0;
        while (cb_obj.active){
            if (len>=endlen){
                loopcount++;
                if(loopcount==2){
                    cb_obj.active=false;
                    break;
                }
                len=minlen;
            }
            len = len+864000000;
            slider.value = len;
            await sleep(4)
        }
    }
    run();
''')
#loops through slider twice (only looks like once if starting at the end)
#adds 10 days at a time 
#sleeps 4 milliseconds inbetween each increment 

button = Toggle(label='▶\uFE0E', button_type='success') 
#\uFE0E forces non emoji rendering (only on some browsers)
button.js_on_click(loopchange)

arrangement = layout([slider,button], tabs)
show(arrangement)
