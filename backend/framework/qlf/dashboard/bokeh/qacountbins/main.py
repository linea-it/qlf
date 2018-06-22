import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label, FixedTicker
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

from bokeh.io import output_notebook
import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description, get_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist, html_table

import numpy as np
import logging

#Additional imports:
from bokeh.models.widgets import Div


logger = logging.getLogger(__name__)

# =============================================
# THIS comes from INTERFACE
#
args = get_url_args(curdoc)

try:
    selected_process_id = args['process_id']
    selected_arm = args['arm']
    selected_spectrograph = args['spectrograph']
except:
    sys.exit('Invalid args')

# ============================================
#  THIS READ yaml files
#

cam = selected_arm+str(selected_spectrograph)
try:
    lm = get_scalar_metrics(selected_process_id, cam)
    metrics, tests  = lm['results']['metrics'], lm['results']['tests']
except:
    sys.exit('Could not load metrics')

countbins = metrics['countbins']

print(metrics['snr'].keys())

# ============================================
# THIS: Given the set up in the block above, 
#       we have the bokeh plots


qlf_fiberid = np.arange(0, 500)

# prevent to broke if the file was not generated by ql
try:
    snr = metrics['snr']
except:
    snr = {'ELG_FIBERID': [], 'QSO_FIBERID': [],
           'LRG_FIBERID': [], 'STAR_FIBERID': []}
try:
    skycont = metrics['skycont']
except:
    skycont = {'SKYFIBERID': []}
# marking type of objects:
try:
    obj_type = []
    for i in qlf_fiberid:
    
        if i in snr['ELG_FIBERID']:
            obj_type.append('ELG')
        elif i in snr['QSO_FIBERID']:
            obj_type.append('QSO')
        elif i in snr['LRG_FIBERID']:
            obj_type.append('LRG')
        elif i in snr['STAR_FIBERID']:
            obj_type.append('STAR')
        elif i in skycont['SKYFIBERID']:
            obj_type.append('SKY')
        else:
            obj_type.append('UNKNOWN')
except:
    logger.info('Problems in obj sorter')
    obj_type=['']*500
# ---------------------------------


hist_tooltip=""" 
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
            <span style="font-size: 13px; color: #515151;">@status</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER ID: </span>
            <span style="font-size: 13px; color: #515151;">@fiberid</span>
        </div>
    </div>
        """
y=np.array(countbins['GOOD_FIBER'])
x=np.array(range(len(countbins['GOOD_FIBER'])))
hist_hover = HoverTool(tooltips=hist_tooltip)
hist_source = ColumnDataSource(
                data={'goodfiber': y,
                      'fiberid' : x,
                        'segx0': x -0.4,
                        'segx1': x +0.4,
                        'segy0': y ,
                        'segy1': y ,
                        'status': ['GOOD' if i==1 else 'BAD' for i in y],
                        'x1': snr['RA'],
                        'y1': snr['DEC'],   
                    'QLF_FIBERID': qlf_fiberid,
                    'OBJ_TYPE': obj_type,
                    'color': ['#319b5c' if i ==1 else '#282828' for i in countbins['GOOD_FIBER']]
                     })


p = Figure(tools = [hist_hover,"pan,wheel_zoom,  box_zoom, lasso_select, reset, crosshair, tap"],
            plot_width=700, plot_height=300, y_range = Range1d(-.1,1.1),
            x_axis_label='Fiber', y_axis_label=' Fiber Status' )
from bokeh.models.glyphs import Segment

seg=Segment(x0='segx0', x1='segx1', y0='segy0',y1='segy1', line_width=2, line_color='#1e90ff')

p.add_glyph(hist_source, seg)
#(x0='fiberid', top='goodfiber', width=0.5, source=hist_source        )
label = Label(x=330, y=0.7, x_units='data', y_units='data',
                 text='NGOOD_FIBER: {}'.format(countbins['NGOODFIB']), render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)

p.yaxis.ticker=FixedTicker(ticks=[0,1])
p.yaxis.major_label_overrides = {'0':'bad', '1':'good'}
p.add_layout(label)


#----------------
# Wedge
count_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
            <span style="font-size: 13px; color: #515151">@status</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
            <span style="font-size: 13px; color: #515151;">@x1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
            <span style="font-size: 13px; color: #515151;">@y1</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
            <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
        </div>
    </div>
"""



hover = HoverTool(tooltips=count_tooltip)

#from dashboard.bokeh.helper import get_palette
#my_palette = get_palette('Reds')
#mapper = LinearColorMapper(palette=my_palette,
#                           low=0.98*np.min(peakcount),
#                           high=1.02*np.max(peakcount))

radius = 0.013#0.015
radius_hover = 0.015#0.0165

# axes limit
xmin, xmax = [min(snr['RA'][:]), max(snr['RA'][:])]
ymin, ymax = [min(snr['DEC'][:]), max(snr['DEC'][:])]
xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
left, right = xmin -xfac, xmax+xfac
bottom, top = ymin-yfac, ymax+yfac

p2 = Figure(title='GOOD FIBERS'#: sum of counts in peak regions '
        , x_axis_label='RA', y_axis_label='DEC'
        , plot_width=601, plot_height=550            
        , tools=[hover, "pan,box_zoom,reset,lasso_select,crosshair, tap"], toolbar_location="right")

# Color Map
p2.circle('x1', 'y1', source=hist_source, name="data", radius=radius,
         fill_color= {'field':'color'}, #{'field': 'peakcount', 'transform': mapper},
         line_color='black', line_width=0.3,
         hover_line_color='red')

# marking the Hover point
p2.circle('x1', 'y1', source=hist_source, name="data", radius=radius_hover, 
        hover_fill_color={'field': 'color'}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')






'''
hist_tooltip = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Frequency: </span>
            <span style="font-size: 13px; color: #515151">@hist</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">sigma: </span>
            <span style="font-size: 13px; color: #515151;">[@left, @right]</span>
        </div>
    </div>
"""
name_hi = 'NBINSHI'
name_med = 'NBINSMED'
name_low = 'NBINSLO'


hover = HoverTool(tooltips=hist_tooltip)
hover2 = HoverTool(tooltips=hist_tooltip)
hover3 = HoverTool(tooltips=hist_tooltip)
bins_hi, bins_med, bins_low = 'sqrt', 'sqrt', 'sqrt' #‘fd’ (Freedman Diaconis Estimator), ‘doane’, sturges

# ===
hist_hi, edges_hi = np.histogram(countbins[name_hi], bins = bins_hi)
source_hi = ColumnDataSource(data={
    'hist':hist_hi,
    'bottom':[0] *len(hist_hi),
    'left':edges_hi[:-1],
    'right':edges_hi[1:]
})

# ===
hist_med, edges_med = np.histogram(countbins[name_med], bins = bins_med)
source_med = ColumnDataSource(data={
    'hist':hist_med,
    'bottom':[0] *len(hist_med),
    'left':edges_med[:-1],
    'right':edges_med[1:]
})

# ===
hist_low, edges_low = np.histogram(countbins[name_low], bins = bins_low)
source_low = ColumnDataSource(data={
    'hist':hist_low,
    'bottom':[0] *len(hist_low),
    'left':edges_low[:-1],
    'right':edges_low[1:]
})



phi = Figure(title='NBINSHI',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

phi.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_hi, 
        fill_color="dodgerblue", line_color="black", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

pmed = Figure(title='NBINSMED',tools=[hover2,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")

pmed.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_med, 
        fill_color="lightgreen", line_color="black", alpha=0.8,
       hover_fill_color='green', hover_line_color='black', hover_alpha=0.8)


plow = Figure(title='NBINSLOW',tools=[hover3,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label='Frequency', x_axis_label='COUNTBINS', background_fill_color="white")


plow.quad(top='hist', bottom='bottom', left='left', right='right',
       source=source_low, fill_color="tomato", line_color="black", alpha=0.8,
       hover_fill_color='red', hover_line_color='black', hover_alpha=0.8)
# ------------------
# Text Infos
html_str="""
<style>
    table {
        font-family: arial, sans-serif;
        font-size: 12px;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #dddddd;
                text-align:center;
    }
    tr:{text-align:center;}
</style>

<div  style="text-align:center;padding-left:20px;padding-top:10px;">
<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>CUT-OFF LOW</td>
    <td> > param0</td>
  </tr>
  <tr>
    <td>CUT-OFF MEDIUM</td>
    <td> > param1</td>
  </tr>
  <tr>
    <td>CUT-OFF HIGH</td>
    <td> > param2</td>
  </tr>
    <tr>
        <th colspan="2"; style="text-align:center">GOOD FIBERS RANGES:</th>
    </tr>
    <tr>
        <td> NORMAL RANGE</td>
        <td> param3</td>
    </tr>
    <tr>
        <td> WARNING RANGE </td>
        <td> param4</td>
    </tr>

</table>
</div>

"""
txt_keys=['CUTLO','CUTMED','CUTHI','NGOODFIB_NORMAL_RANGE', 'NGOODFIB_WARN_RANGE']
for i in range(5):
    html_str=html_str.replace('%s%s'%("param",str(i)), str(tests['countbins'][txt_keys[i]]) )

div=Div(text=html_str, 
        width=400, height=200)
# ---------



# plow.legend.location = "top_left"
# layout = gridplot( [phi,pmed,plow,None], ncols=2, plot_width=600, plot_height=600)

layout_plot = gridplot( [plow,pmed,phi,div], ncols=2, responsive=False, plot_width=600, plot_height=600)
'''

nrg = tests['countbins']['NGOODFIB_NORMAL_RANGE']
wrg = tests['countbins']['NGOODFIB_WARN_RANGE']
ngood = countbins['NGOODFIB']
fracgood= ngood/500. -1.
tb = html_table(names=['NGOODFIB', 'FRACTION BAD'], vals=[ngood, str(fracgood*100)+' %' ], nrng=nrg, wrng=wrg  )
tbinfo=Div(text=tb, width=600, height=200)


#print(wrg)
layout_plot=p
info_col=Div(text=write_description('countbins'), width=1200)
layout = column(widgetbox(info_col), tbinfo, p2, layout_plot)#)


# End of Bokeh Block
curdoc().add_root(layout)
curdoc().title = "COUNTBINS"

