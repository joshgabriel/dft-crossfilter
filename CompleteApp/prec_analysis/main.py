import os
from os.path import dirname, join

from collections import OrderedDict
import pandas as pd
import numpy as np

import json

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column, gridplot, layout
from bokeh.models import Select, Div, Column, \
HoverTool, ColumnDataSource, Button, RadioButtonGroup,\
MultiSelect, RangeSlider
#from bokeh.models.widgets import RangeSlider
from bokeh.plotting import figure
from bokeh import mpl
from precision.precisions import DatabaseData

import requests

plottables =  ['k-point', 'value', 'perc_precisions']

x_select = Select(title='X-Axis', value='k-point', options=plottables)

y_select = Select(title='Y-Axis', value='value', options=plottables)

############## Header Content from description.html  #################

content_filename1 = join(dirname(__file__), "UserInstructions.html")

Desc_C1 = Div(text=open(content_filename1).read(),
                  render_as_text=False, width=600)

content_filename2 = join(dirname(__file__), "UserInstructions.html")

Desc_C2 = Div(text=open(content_filename2).read(),
                  render_as_text=False, width=600)

content_filename3 = join(dirname(__file__), "UserInstructions.html")

Desc_C3 = Div(text=open(content_filename1).read(),
                  render_as_text=False, width=600)

content_filename4 = join(dirname(__file__), "UserInstructions.html")

Desc_C4 = Div(text=open(content_filename2).read(),
                  render_as_text=False, width=600)

######### APP CROSSFILTER ##########################


# decide if all columns or crossfilter down to sub properties
#source_data = pd.DataFrame({})#ColumnDataSource(data=dict())

class CrossFiltDFs():

    def __init__(self,query_dict={'code':'VASP','exchange':'PBE',\
                                  'element':'Au','structure':'fcc','properties':'B'},plot_data=None):

        self.query_dict = query_dict
        self.plot_data = plot_data

    def crossfilter_by_tag(self,df, tag):
        """
        a crossfilter that can recursivly update the unique options
        in the UI based on prioir selections

        returns crossfiltered by tag crossfilter {'element': 'Ag'}
        """
        col,spec= list(tag.items())[0]
        return df[df[col]==spec]

    # The crossfilter widgets
    def update(self, attr, old, new):
       print ('Attribute', attr, 'OLD', old, 'NEW', new)
       print ('executes here on update')#, exchange_df)

    def update_code(self):
        """
        update for the code selection
        """
        print ('update code')
        self.query_dict.update({'code':code.value})

    def update_exchange(self):
        """
        update the exchange
        """
        print ('update exchange')
        self.query_dict.update({'exchange':exchange.value})

    def update_element(self,new):
        print ('Updating element down selection for properties',element.active[0])
        self.query_dict.update({'element':element.active[0]})

    def update_struct(self):
       print ('Updating struct down selection for element')
       self.query_dict.update({'structure':struct.value})
       print ('Updating ptable with structure selection')
       print ('finished callback to update layout')

    def update_prop(self):
       self.properties = prop.value

    def update_kpoints(self):
        pass

    def update_x(self):
        self.x = x.value
        pass

    def update_y(self):
        self.y = y.value
        pass

    def update_range(self):
        pass

    def query_api(self,endpoint):
        query_dict ={k:v for k,v in self.query_dict.items() if k!='properties'}
        self.properties = self.query_dict['properties']
        r = requests.post(url='http://www.dftbenchmarkmgi.com:7200/bench/v1/query_{}'.\
                          format(endpoint),data=json.dumps(self.query_dict))
        ListOfDicts = r.json()['content']
        self.plot_data = pd.concat([pd.DataFrame({k:[ld[k]] for k in list(ld.keys())}) for ld in ListOfDicts])


    def plot_prec_value1(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_api(endpoint='evk')
       layout_doc.children[5] = self.plot_pade_figure()

    def plot_prec_value2(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_api(endpoint='evk')
       layout_doc.children[6] = self.plot_pade_figure()

    def plot_prec_value3(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_api(endpoint='evk')
       layout_doc.children[7] = self.plot_pade_figure()

    def plot_prec_value4(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_api(endpoint='evk')
       layout_doc.children[8] = self.plot_pade_figure()

    def plot_pade_figure(self):
        """
        method which plots multiple curves of different color
        on the same bokeh figure canvas. Will receive query results from the evk
        end point on the E0k, V0k, Bk, BPk, kpoints data. x is always kpoints data log scaled
        """
        # receive a dict of datasets: {'Plot1':{'Dsett1':DFrame, 'x_title': None, 'y_title': None,
        # 'Characteristic':'VASP_PBE_Al_fcc_B'}, 'Plot2':{'x':[],'y':[], 'x_title': None, 'y_title': None}}

        #def color_marker_divider(characteristics):
        #    cm_keys= {'00':('red','*'),'01':('red','-.-'),'02':('red','*'),'03':('red','^'),\
        #     '10':('blue','*'),'11':('blue','-.-'),'12':('blue','*'),'13':('blue','^')
        #     }
        #    DictCharacters = \
        #    [{n:att for n,att in enumerate(c.split('_'))} for c in characteristics]
            # one or two char value different and same code and exchange: same color different marker
            # else different color and marker.
        #    return cm_keys
        kw = {}
        kw['title'] = 'Pade Analysis Plots'
        kw['x_axis_type'] = 'log'
        #color_marker_divider(characteristics)
        #for dset in datasets:
        data_analysis = DatabaseData(dataframe=self.plot_data)
        print (data_analysis.dataframe.columns)
        data_analysis.run_pade_through_R(rscript='./prec_analysis/birch',get_inits_ev=True)
        data_analysis.create_precisions()
        fig_obj = data_analysis.create_pade_bokeh_compat(properties=self.properties)
        #c,m = color_marker_divider(characteristics)['00']
        p = mpl.to_bokeh(fig_obj)
        return p

    def create_figure_new(self):
        """
        create a new multi-figure canvas
        """
        kw = {}
        self.p = figure(plot_height=300, plot_width=300, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
        self.p.circle(x=[0],y=[0])
#        self.p2 = figure(plot_height=300, plot_width=300, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
#        self.p2.circle(x=[0],y=[0])
#        self.p3 = figure(plot_height=300, plot_width=300, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
#        self.p3.circle(x=[0],y=[0])
#        self.p4 = figure(plot_height=300, plot_width=300, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
#        self.p4.circle(x=[0],y=[0])

    def multi_precisions_correlate(self, datasets):
        """
        method which allows the user to plot various precisions
        against each other. Also prints out the M-value and intercepts
        of precision at 1 meV/atom, 0.1 meV/atom and 0.01 meV/atom
        """
        pass

    def kpoints_interactive_selector(self, dataset):
        """
        method which creates a pareto optimal plot for the chosen structure, material,
        code and exchange and with the user input of desired precision returns
        the kpoints per atom choice.
        """
        pass

    def pade_visualize(self,dataset):
        """
        method which creates the Pade contour interpolation over the
        raw evk data. Receives query result from the evk endpoint
        """
        pass

    def create_figure(self,dataset,datplot='Init',plot_type=None):
        """
        figure and plot creation for a given dataset
        TODO: enable support for multiple selection
        refactor to a simple figure creator and
        add helper functions for the plots
        """
        kw = dict()

        x_title = x_select.value.title() + ' Density per atom'

        # hack for labels now

        if isinstance(dataset,pd.DataFrame):
          if np.unique(list(dataset['properties']))[0]=='B':
             y_title = 'Bulk Modulus (GPa) '+y_select.value.title()
          elif np.unique(list(dataset['properties']))[0]=='dB':
             y_title = 'dB/dP '+y_select.value.title()
          elif np.unique(list(dataset['properties']))[0]=='v0':
             y_title = 'Volume per atom (A^3) '+y_select.value.title()
          elif np.unique(list(dataset['properties']))[0]=='E0':
             y_title = 'DFT Energy per atom (eV/atom) '+y_select.value.title()
        else:
             y_title = 'Pade Prediction'

        kw['title'] = "%s vs %s" % (y_title, x_title)

        #if x_select.value=='k-point':
        kw['x_axis_type'] = 'log'

        if x_select.value == 'perc_precisions' and y_select.value == 'perc_precisions':
          kw['y_axis_type'] = 'log'

        self.p = figure(plot_height=600, plot_width=800, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)

        # sets the axes
        self.p.xaxis.axis_label = x_title
        self.p.yaxis.axis_label = y_title


        #if x_select.value in continuous:
        self.p.xaxis.major_label_orientation = pd.np.pi / 4


        #print (dataset)
        if datplot=='Init':
           # if data is to be plotted
           xs = [1,2,3,4]#dataset[x_select.value].values
           ys = [1,2,3,4]#dataset[y_select.value].values
           self.xs_init = xs
           self.ys_init = ys

           self.p.scatter(x=xs, y=ys)#, alpha=1.0, hover_color='blue', hover_alpha=1.0)
           return self.p

        elif datplot == 'Add':
           # add a plot to figure, from statistical analysis
           if plot_type == 'plot_pade':

               #pade_order = self.analysis_results['Order']
               #pade_extrapolate = self.analysis_results['Extrapolate']
               #print (pade_extrapolate, float(pade_extrapolate))

               # create precisions based on the extrapolate
               #print (self.add_data)
               xs = self.add_data[0]
               ys = self.add_data[1]#[abs(y-pade_extrapolate) for y in self.ys_init]
               #print (ys)
               # print (xs,ys,len(xs),len(ys))
               print ("Plots a line supposedly")
               #print (len(self.ys_init), len(ys))
               #l = min([len(self.ys_init), len(ys), len(self.xs_init),len(xs)])
               #self.plot_layout.scatter(x=self.xs_init[0:l], y=self.ys_init[0:l])#, alpha=1.0, hover_color='blue', hover_alpha=1.0)
               #print (type(self.plot_layout))
               #self.p.self.plot
               self.p = figure(plot_height=600, plot_width=800, tools='pan,wheel_zoom,box_zoom,reset,box_zoom, hover', **kw)
               print('executes till re-figure')
               self.p.circle(x=self.xs_init,y=self.ys_init)
               print('executes till circle')
               self.p.line(x=xs, y=ys, line_color='red')
               #self.p.line_color='red'
               print('executes till line')
               return self.p

        else:
          # clear the figure by plotting an empty figure
          xs = []
          ys = []
          self.p = figure(plot_height=600, plot_width=800, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
          self.p.scatter(x=xs, y=ys)#, alpha=1.0, hover_color='blue', hover_alpha=1.0)
          return self.p


    def clear_crossfilter(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.plot_data = None
        layout.children[6] = self.create_figure(self.plot_data)

    def analysis_callback(self):
        """
        calls the Pade analysis on the current plot data
        TODO:
        NOTE: check if this is a data set that is a single scatter
        FEATUREs that could be added: plot the Pade for multiple selections
        """
        print ('called Pade analysis')
        # writes out the crossfiltered plot data on the server
        crossfilt = self.plot_data[['k-point','value']]
        crossfilt.columns=['Kpt','P']
        crossfilt.to_csv('crossfilter_app/Rdata.csv')
        print ('wrote out data file')
        os.system('Rscript crossfilter_app/non_err_weighted_nls.R')
        self.analysis_results = pd.read_csv('crossfilter_app/Result.csv')
        #self.add_data = [ list(self.xs_init), list(self.predict_results['Preds....c.predict.m2..']) ]
        ext_values = list(self.analysis_results['Extrapolate....extrapolates'])
        error_values = list(self.analysis_results['Error....errors'])
        self.ext_min_error = ext_values[error_values.index(min(error_values))]
        print ('executed R script on crossfiltered data')
        if error_values.index(min(error_values))==0:
            self.predict_results = pd.read_csv('crossfilter_app/Pade1.csv')
            self.add_data = [list(self.predict_results['Px....x_plot']), list(self.predict_results['Py....pade1.x_plot.'])]
        elif error_values.index(min(error_values))==1:
            self.predict_results = pd.read_csv('crossfilter_app/Pade2.csv')
            self.add_data = [list(self.predict_results['Px....x_plot']), list(self.predict_results['Py....pade2.x_plot.'])]

        print ('ADD DATA', self.add_data)
        layout.children[4] = self.create_figure(self.add_data, datplot='Add', plot_type='plot_pade')

def update():
    pass
    #source_data = CF.plot_data

# initialize the crossfilter instance

# define the selection widgets for code, exchange,
# TODO: enable widgets that support multi-selection
# Elements selection widget from a periodic table
CF1 = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE','structure':'fcc','element':'Pt','properties':'B'})
CF2 = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE','structure':'fcc','element':'Pt', 'properties':'B'})
CF3 = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE','structure':'fcc','element':'Pt', 'properties':'B'})
CF4 = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE','structure':'fcc','element':'Pt', 'properties':'B'})
# first query
CF1.query_api(endpoint='evk')
CF2.query_api(endpoint='evk')
CF3.query_api(endpoint='evk')
CF4.query_api(endpoint='evk')


# for the first table to display VASP PBE all structures Pade extrapolates for all properties
# as a bonus with some error bar too

#### PLOT 1
codes = ['DMol3','VASP']
code = Select(title='Code_1', value=codes[1], options=codes)
code.on_change('value', lambda attr, old, new: CF1.update_code())

exchanges = ['LDA','PBE']
exchange = Select(title='ExchangeCorrelation_1', value=exchanges[1], options=exchanges)
exchange.on_change('value', lambda attr, old, new: CF1.update_exchange())

structures = ['fcc','bcc','hcp']
struct = Select(title='Structure_1', value=structures[1], options=structures)
struct.on_change('value', lambda attr, old, new: CF1.update_struct())

_elements = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element = Select(title='Metals_1', value=_elements[0], options=_elements)
element.on_change('value', lambda attr, old, new: CF1.update_element())

properties = ['B','dB','V0','E0']
prop = Select(title='Properties_1', value=properties[0], options=properties)
prop.on_change('value', lambda attr, old, new: CF1.update_prop())

#range_slider_lowK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

apply_crossfilter = Button(label='Values vs. Kpoints')
apply_crossfilter.on_click(CF1.plot_prec_value1())

clean_crossfilter = Button(label='Clear')
clean_crossfilter.on_click(CF1.clear_crossfilter())



#### PLOT 2

codes2 = ['DMol3','VASP']
code2 = Select(title='Code_2', value=codes[1], options=codes2)
code2.on_change('value', lambda attr, old, new: CF2.update_code())

exchanges2 = ['LDA','PBE']
exchange2 = Select(title='ExchangeCorrelation_2', value=exchanges[1], options=exchanges2)
exchange2.on_change('value', lambda attr, old, new: CF2.update_exchange())

structures2 = ['fcc','bcc','hcp']
struct2 = Select(title='Structure_2', value=structures[1], options=structures2)
struct2.on_change('value', lambda attr, old, new: CF2.update_struct())

_elements2 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element2 = Select(title='Metals_2', value=_elements[0], options=_elements2)
element2.on_change('value', lambda attr, old, new: CF2.update_element())

properties2 = ['B','dB','V0','E0']
prop2 = Select(title='Properties_2', value=properties[0], options=properties2)
prop2.on_change('value', lambda attr, old, new: CF2.update_prop())

#range_slider_lowK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

apply_crossfilter2 = Button(label='Values vs. Kpoints')
apply_crossfilter2.on_click(CF2.plot_prec_value2())

clean_crossfilter2 = Button(label='Clear')
clean_crossfilter2.on_click(CF2.clear_crossfilter)

###### PLOT 3

codes3 = ['DMol3','VASP']
code3 = Select(title='Code_3', value=codes[1], options=codes3)
code3.on_change('value', lambda attr, old, new: CF3.update_code())

exchanges3 = ['LDA','PBE']
exchange3 = Select(title='ExchangeCorrelation_3', value=exchanges[1], options=exchanges3)
exchange3.on_change('value', lambda attr, old, new: CF3.update_exchange())

structures3 = ['fcc','bcc','hcp']
struct3 = Select(title='Structure_3', value=structures[1], options=structures3)
struct3.on_change('value', lambda attr, old, new: CF3.update_struct())

_elements3 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element3 = Select(title='Metals_3', value=_elements[0], options=_elements3)
element3.on_change('value', lambda attr, old, new: CF3.update_element())

properties3 = ['B','dB','V0','E0']
prop3 = Select(title='Properties_3', value=properties[0], options=properties3)
prop3.on_change('value', lambda attr, old, new: CF3.update_prop())

apply_crossfilter3 = Button(label='Values vs. Kpoints')
apply_crossfilter3.on_click(CF3.plot_prec_value3())

#range_slider_lowK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_lowK3.on_change('value',lambda attr,old,new: CF.update_range())
#range_slider_medK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_medK3.on_change('value',lambda attr,old,new: CF.update_range())
#range_slider_highK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")
#range_slider_highK3.on_change('value',lambda attr,old,new: CF.update_range())

clean_crossfilter3 = Button(label='Clear')
clean_crossfilter3.on_click(CF3.clear_crossfilter())

###### PLOT 4

codes4 = ['DMol3','VASP']
code4 = Select(title='Code_3', value=codes[0], options=codes4)
code4.on_change('value', lambda attr, old, new: CF4.update_code())

exchanges4 = ['LDA','PBE']
exchange4 = Select(title='ExchangeCorrelation_3', value=exchanges[0], options=exchanges4)
exchange4.on_change('value', lambda attr, old, new: CF4.update_exchange())

structures4 = ['fcc','bcc','hcp']
struct4 = Select(title='Structure_3', value=structures[-2], options=structures4)
struct4.on_change('value', lambda attr, old, new: CF4.update_struct())

_elements4 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element4 = Select(title='Metals_3', value=_elements[0], options=_elements3)
element4.on_change('value', lambda attr, old, new: CF4.update_element())

properties4 = ['B','dB','V0','E0']
prop4 = Select(title='Properties_3', value=properties[0], options=properties4)
prop4.on_change('value', lambda attr, old, new: CF4.update_prop())

apply_crossfilter4 = Button(label='Values vs. Kpoints')
apply_crossfilter4.on_click(CF4.plot_prec_value4())

#range_slider_lowK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

clean_crossfilter4 = Button(label='Clear')
clean_crossfilter4.on_click(CF4.clear_crossfilter())

# a new widget that allows for choosing the minimum number of k-points needed to
# evaluate a Pade extrapolate within 2 % of the Pade with all the points
#all_kpts = CF.plot_data['k-point']

# Low
#low_kpt = all_kpts.quantile(0.33)
#Low_Kpoints = Select(title='Low K-points', value=low_kpt, options=list(all_kpts))
#Low_Kpoints.on_change('value', lambda attr, old, new: CF.update_kpoints())
#range_slider_point1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")

# medium
#med_kpt = all_kpts.quantile(0.66)
#Medium_Kpoints = Select(title='Medium K-points', value=med_kpt, options=list(all_kpts))
#Medium_Kpoints.on_change('value', lambda attr, old, new: CF.update_kpoints())
#range_slider_point2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")

# High kpoints
#high_kpt = max(all_kpts)
#High_Kpoints = Select(title='High K-points', value=high_kpt, options=list(all_kpts))
#High_Kpoints.on_change('value', lambda attr, old, new: CF.update_kpoints())
#range_slider_point3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

## Point selection

#analyse_crossfilt = Button(label='PadeAnalysis')
#analyse_crossfilt.on_click(CF.analysis_callback)

#CF_init = CrossFiltDFs()

CF1.create_figure_new()
CF2.create_figure_new()
CF3.create_figure_new()
CF4.create_figure_new()

#Fig_canvas = gridplot([CF.p1, CF.p2, CF.p3, CF.p4])
controls1 = widgetbox([code, exchange, struct, element, prop, apply_crossfilter],width=300)
                       #range_slider_lowK1, range_slider_medK1, range_slider_highK1], width=300)
controls2 = widgetbox([code2, exchange2, struct2, element2, prop2,apply_crossfilter2],width=300)
                        #range_slider_lowK2, range_slider_medK2, range_slider_highK2, width=300)
controls3 = widgetbox([code3, exchange3, struct3, element3, prop3, apply_crossfilter3], width=300)
                       #range_slider_lowK3, range_slider_medK3, range_slider_highK3], width=300)
controls4 = widgetbox([code4, exchange4, struct4, element4, prop4, apply_crossfilter4], width=300)
                       #range_slider_lowK4, range_slider_medK4, range_slider_highK4], width=300)
#controls_final = widgetbox([prop, x_select, y_select, apply_crossfilter, analyse_crossfilt, clean_crossfilter], width=400)
#print ('Initial init figure data', type(CF_init.prop_df))
layout_doc = layout([Desc_C1], [controls1, controls2, controls3,controls4], [CF1.p, CF2.p, CF3.p, CF4.p])#Desc_C1, controls1, Desc_C2, controls2,\
                    #Desc_C3, controls3, Desc_C4, controls_final)

#layout_doc = layout([description1],\
#                    [ptable1],\
#                    [description2],\
#                    row([element,code,exchange,struct]),\
#                    row([element,code,exchange,struct]),\
#                    row([element,code,exchange,struct]),\
#                    row([element,code,exchange,struct]),\
#                    sizing_mode='stretch_both'
#                    )
#column(description1, ptable1, description2, controls1, ptable2, controls2)

#CF.update_ptable()

print ('executed till here')

#z = Select(title='Z-Axis', value='None', options=plottables)
#z.on_change('value', update)
curdoc().add_root(layout_doc)
curdoc().title = "DFT Benchmark"
update()
