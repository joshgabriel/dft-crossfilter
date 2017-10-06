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
MultiSelect
#from bokeh.models.widgets import RangeSlider
from bokeh.plotting import figure
from bokeh import mpl
from precision.precisions import DatabaseData

import requests

print ('Does something after imports')

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
        print ('Updating element down selection for properties',element.value)
        self.query_dict.update({'element':element.value})

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
        if self.properties == 'dB':
            self.properties = 'BP'
        r = requests.post(url='http://0.0.0.0:6400/bench/v1/query_{}'.\
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
       self.query_dict={'code':code.value,'exchange':exchange.value,\
                    'structure':struct.value,'element':element.value,'properties':prop.value}
       print ('POSTING', self.query_dict)
       self.query_api(endpoint='evk')
       layout_doc.children[2].children[0] = self.plot_pade_figure()

    def clear_crossfilter1(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[2].children[0] = self.p

    def plot_prec_value2(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_dict={'code':code2.value,'exchange':exchange2.value,\
                    'structure':struct2.value,'element':element2.value,'properties':prop2.value}
       print ('POSTING', self.query_dict)
       self.query_api(endpoint='evk')
       layout_doc.children[2].children[1] = self.plot_pade_figure()

    def clear_crossfilter2(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[2].children[1] = self.p

    def plot_prec_value3(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_dict={'code':code3.value,'exchange':exchange3.value,\
                    'structure':struct3.value,'element':element3.value,'properties':prop3.value}
       print ('POSTING', self.query_dict)
       self.query_api(endpoint='evk')
       layout_doc.children[2].children[2] = self.plot_pade_figure()

    def clear_crossfilter3(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[2].children[2] = self.p

    def plot_prec_value4(self):
       """
       calls the plotting operation by querying the
       evk endpoint and returning a single evk packet
       of single material structure code exchange to
       self.plot_data.
       This controls the first plot canvas
       """
       self.query_dict={'code':code4.value,'exchange':exchange4.value,\
                        'structure':struct4.value,'element':element4.value,'properties':prop4.value}
       print ('POSTING', self.query_dict)
       self.query_api(endpoint='evk')
       layout_doc.children[2].children[3] = self.plot_pade_figure()

    def clear_crossfilter4(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[2].children[3] = self.p

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
        #color_marker_divider(characteristics)
        #for dset in datasets:
        data_analysis = DatabaseData(dataframe=self.plot_data)
        print (data_analysis.dataframe.columns)
        data_analysis.run_pade_through_R(rscript='./prec_analysis/birch',get_inits_ev=True)
        data_analysis.create_precisions()
        data_analysis.extract_pade_curve()
        x_eos_kpts, y_eos, xs_err, ys_err, x_pade_kpts, y_pade = \
        data_analysis.create_pade_bokeh_compat(properties=self.properties)
        #c,m = color_marker_divider(characteristics)['00']
        print (type(self.properties), self.properties)
        if self.properties == 'B':
            ext = data_analysis.Bp
            print ('HERE AT PROPERTIES', ext, type(ext))
        elif self.properties == 'BP':
            ext = data_analysis.BPp
        elif self.properties == 'E0':
            ext = data_analysis.E0p
        elif self.properties == 'V0':
            ext = data_analysis.V0p
        p = figure(plot_height=400, plot_width=400,tools="pan,wheel_zoom,box_zoom,reset,previewsave",\
        x_axis_type="log", x_axis_label='K-points per atom',  title='Pade Extrapolate of {0} is {1}'.format(self.properties, str(ext)) )
        p.xaxis.axis_label = 'K-points per atom'
        p.line(x_pade_kpts, y_pade, color='red')
        p.circle(x_eos_kpts, y_eos,color='blue',size=5, line_alpha=0)
        p.multi_line(xs_err, ys_err, color='black')
        #p.x_axis_label = 'K-points per atom'
        if self.properties == 'B':
            p.yaxis.axis_label = 'Bulk Modulus B (GPa)'
        elif self.properties == 'dB':
            p.yaxis.axis_label = 'Bulk Modulus Pressure Derivative'
        elif self.properties == 'E0':
            p.yaxis.axis_label = 'DFT Energy (eV/atom)'
        elif self.properties == 'V0':
            p.yaxis.axis_label = 'Volume (A^3/atom)'

        return p

    def create_figure_new(self):
        """
        create a new multi-figure canvas
        """
        kw = {}
        self.p = figure(plot_height=400, plot_width=400, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
        self.p.circle(x=[0],y=[0])


    def plot_precision_figure(self):
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

        data_analysis = DatabaseData(dataframe=self.plot_data)
        prop_data, energy_data, M, C, pred_energy, pred_property = \
        data_analysis.create_precision_bokeh_compat(self.prop_data, self.energy_data, properties=self.properties)
        p = figure(plot_height=400, plot_width=400,tools="pan,wheel_zoom,box_zoom,reset,previewsave",\
        x_axis_type="log", y_axis_type="log", x_axis_label='Energy Convergence (meV/atom)',  title='Slope M is {0}'.format(str(M)) )
        p.line(pred_energy, pred_property, color='red')
        p.circle(energy_data, prop_data, color='blue',size=5, line_alpha=0)
        #p.multi_line(xs_err, ys_err, color='black')
        if self.properties == 'B':
            p.yaxis.axis_label = 'Bulk Modulus B (%)'
        elif self.properties == 'dB':
            p.yaxis.axis_label = 'Bulk Modulus Pressure Derivative (%)'
        elif self.properties == 'Multiple':
            p.yaxis.axis_label = "V0, B, B' (%)"
        elif self.properties == 'V0':
            p.yaxis.axis_label = 'Volume (%)'

        return p

    def multi_precisions_correlate1(self):
        """
        method which allows the user to plot various precisions
        against each other. Also prints out the M-value and intercepts
        of precision at 1 meV/atom, 0.1 meV/atom and 0.01 meV/atom
        """
        self.query_dict={'code':code.value,'exchange':exchange.value,\
                        'structure':struct.value,'element':element.value,'properties':prop4.value}
        print ('POSTING', self.query_dict)
        if not self.query_dict['properties'] == 'Multi':
            self.query_api(endpoint='precvalue')
            self.prop_data = self.plot_data['s{}k'.format(self.properties)]
            self.energy_data = self.plot_data['sE0k'.format(self.properties)]

        layout_doc.children[2].children[0] = self.plot_precision_figure()
        pass

    def multi_precisions_correlate2(self):
        """
        method which allows the user to plot various precisions
        against each other. Also prints out the M-value and intercepts
        of precision at 1 meV/atom, 0.1 meV/atom and 0.01 meV/atom
        """
        self.query_dict={'code':code2.value,'exchange':exchange2.value,\
                        'structure':struct2.value,'element':element2.value,'properties':prop2.value}
        print ('POSTING', self.query_dict)
        if not self.query_dict['properties'] == 'Multi':
            self.query_api(endpoint='precvalue')
            self.prop_data = self.plot_data['s{}k'.format(self.properties)]
            self.energy_data = self.plot_data['sE0k'.format(self.properties)]
        layout_doc.children[2].children[1] = self.plot_precision_figure()

    def multi_precisions_correlate3(self):
        """
        method which allows the user to plot various precisions
        against each other. Also prints out the M-value and intercepts
        of precision at 1 meV/atom, 0.1 meV/atom and 0.01 meV/atom
        """
        self.query_dict={'code':code3.value,'exchange':exchange3.value,\
                        'structure':struct3.value,'element':element3.value,'properties':prop3.value}
        print ('POSTING', self.query_dict)
        if not self.query_dict['properties'] == 'Multi':
            self.query_api(endpoint='precvalue')
            self.prop_data = self.plot_data['s{}k'.format(self.properties)]
            self.energy_data = self.plot_data['sE0k'.format(self.properties)]

        layout_doc.children[2].children[2] = self.plot_precision_figure()


    def multi_precisions_correlate4(self):
        """
        method which allows the user to plot various precisions
        against each other. Also prints out the M-value and intercepts
        of precision at 1 meV/atom, 0.1 meV/atom and 0.01 meV/atom
        """
        self.query_dict={'code':code4.value,'exchange':exchange4.value,\
                        'structure':struct4.value,'element':element4.value,'properties':prop4.value}
        print ('POSTING', self.query_dict)
        if not self.query_dict['properties'] == 'Multi':
            self.query_api(endpoint='precvalue')
            self.prop_data = self.plot_data
            self.query_dict={'code':code.value,'exchange':exchange.value,\
                        'structure':struct.value,'element':element.value,'properties':'E0'}
            self.query_api(endpoint='precvalue')
            self.energy_data = self.plot_data

        layout_doc.children[2].children[3] = self.plot_precision_figure()


    def kpoints_interactive_selector(self, dataset):
        """
        method which creates a pareto optimal plot for the chosen structure, material,
        code and exchange and with the user input of desired precision returns
        the kpoints per atom choice.
        """
        pass


    def clear_crossfilter(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.plot_data = None
        layout_doc.children[6] = self.create_figure_new()


print ('DOES SOMETHING')

CF1 = CrossFiltDFs()
CF2 = CrossFiltDFs()
CF3 = CrossFiltDFs()
CF4 = CrossFiltDFs()


# for the first table to display VASP PBE all structures Pade extrapolates for all properties
# as a bonus with some error bar too

#### PLOT 1
codes = ['DMol3','VASP']
code = Select(title='Code 1', value='VASP', options=codes)
code.on_change('value', lambda attr, old, new: CF1.update_code())

exchanges = ['LDA','PBE']
exchange = Select(title='ExchangeCorrelation 1', value='PBE', options=exchanges)
exchange.on_change('value', lambda attr, old, new: CF1.update_exchange())

structures = ['fcc','bcc','hcp']
struct = Select(title='Structure 1', value='fcc', options=structures)
struct.on_change('value', lambda attr, old, new: CF1.update_struct())

_elements = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element = Select(title='Metals 1', value='Pt', options=_elements)
element.on_change('value', lambda attr, old, new: CF1.update_element())

properties = ['B','dB','V0','E0']
prop = Select(title='Properties 1', value='E0', options=properties)
prop.on_change('value', lambda attr, old, new: CF1.update_prop())

#range_slider_lowK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK1 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

apply_crossfilter = Button(label='Values vs. Kpoints')
apply_crossfilter.on_click(CF1.plot_prec_value1)

apply_precision = Button(label='Inter-Property Precision')
apply_precision.on_click(CF1.multi_precisions_correlate1)

clean_crossfilter = Button(label='Clear')
clean_crossfilter.on_click(CF1.clear_crossfilter1)

CF1.query_dict={'code':'VASP','exchange':'PBE',\
                'structure':'fcc','element':'Pt','properties':'E0'}


#### PLOT 2

codes2 = ['DMol3','VASP']
code2 = Select(title='Code 2', value='VASP', options=codes2)
code2.on_change('value', lambda attr, old, new: CF2.update_code())

exchanges2 = ['LDA','PBE']
exchange2 = Select(title='ExchangeCorrelation 2', value='PBE', options=exchanges2)
exchange2.on_change('value', lambda attr, old, new: CF2.update_exchange())

structures2 = ['fcc','bcc','hcp']
struct2 = Select(title='Structure 2', value='fcc', options=structures2)
struct2.on_change('value', lambda attr, old, new: CF2.update_struct())

_elements2 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element2 = Select(title='Metals 2', value='Pt', options=_elements2)
element2.on_change('value', lambda attr, old, new: CF2.update_element())

properties2 = ['B','dB','V0','E0']
prop2 = Select(title='Properties 2', value='V0', options=properties2)
prop2.on_change('value', lambda attr, old, new: CF2.update_prop())

#range_slider_lowK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK2 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

apply_crossfilter2 = Button(label='Values vs. Kpoints')
apply_crossfilter2.on_click(CF2.plot_prec_value2)

clean_crossfilter2 = Button(label='Clear')
clean_crossfilter2.on_click(CF2.clear_crossfilter2)

apply_precision2 = Button(label='Inter-Property Precision')
apply_precision2.on_click(CF1.multi_precisions_correlate2)

CF2.query_dict={'code':'VASP','exchange':'PBE',\
                'structure':'fcc','element':'Pt','properties':'V0'}

###### PLOT 3

codes3 = ['DMol3','VASP']
code3 = Select(title='Code 3', value='VASP', options=codes3)
code3.on_change('value', lambda attr, old, new: CF3.update_code())

exchanges3 = ['LDA','PBE']
exchange3 = Select(title='ExchangeCorrelation 3', value='PBE', options=exchanges3)
exchange3.on_change('value', lambda attr, old, new: CF3.update_exchange())

structures3 = ['fcc','bcc','hcp']
struct3 = Select(title='Structure 3', value='fcc', options=structures3)
struct3.on_change('value', lambda attr, old, new: CF3.update_struct())

_elements3 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element3 = Select(title='Metals 3', value='Pt', options=_elements3)
element3.on_change('value', lambda attr, old, new: CF3.update_element())

properties3 = ['B','dB','V0','E0']
prop3 = Select(title='Properties 3', value='B', options=properties3)
prop3.on_change('value', lambda attr, old, new: CF3.update_prop())

apply_crossfilter3 = Button(label='Values vs. Kpoints')
apply_crossfilter3.on_click(CF3.plot_prec_value3)

apply_precision3 = Button(label='Inter-Property Precision')
apply_precision3.on_click(CF1.multi_precisions_correlate3)

clean_crossfilter3 = Button(label='Clear')
clean_crossfilter3.on_click(CF3.clear_crossfilter3)

CF3.query_dict={'code':'VASP','exchange':'PBE',\
                'structure':'fcc','element':'Pt','properties':'B'}



#range_slider_lowK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_lowK3.on_change('value',lambda attr,old,new: CF.update_range())
#range_slider_medK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_medK3.on_change('value',lambda attr,old,new: CF.update_range())
#range_slider_highK3 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")
#range_slider_highK3.on_change('value',lambda attr,old,new: CF.update_range())

###### PLOT 4

codes4 = ['DMol3','VASP']
code4 = Select(title='Code 4', value='VASP', options=codes4)
code4.on_change('value', lambda attr, old, new: CF4.update_code())

exchanges4 = ['LDA','PBE']
exchange4 = Select(title='ExchangeCorrelation 4', value='PBE', options=exchanges4)
exchange4.on_change('value', lambda attr, old, new: CF4.update_exchange())

structures4 = ['fcc','bcc','hcp']
struct4 = Select(title='Structure 4', value='fcc', options=structures4)
struct4.on_change('value', lambda attr, old, new: CF4.update_struct())

_elements4 = ['Al','Au','Sc', 'Ti','V','Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
'Rb', 'Sr','Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag','Cd',
'Cs','Ba','Hf','Ta','W','Re','Os','Ir','Pt','Hg']
element4 = Select(title='Metals 4', value='Pt', options=_elements3)
element4.on_change('value', lambda attr, old, new: CF4.update_element())

properties4 = ['B','dB','V0','E0']
prop4 = Select(title='Properties 4', value='dB', options=properties4)
prop4.on_change('value', lambda attr, old, new: CF4.update_prop())

apply_crossfilter4 = Button(label='Values vs. Kpoints')
apply_crossfilter4.on_click(CF4.plot_prec_value4)

apply_precision4 = Button(label='Inter-Property Precision')
apply_precision4.on_click(CF1.multi_precisions_correlate4)


#range_slider_lowK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Low K-point")
#range_slider_medK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="Medium K-point")
#range_slider_highK4 = RangeSlider(start=-5, end=5, value=(-5,5), step=1, title="High K-point")

clean_crossfilter4 = Button(label='Clear')
clean_crossfilter4.on_click(CF4.clear_crossfilter4)

CF4.query_dict={'code':'VASP','exchange':'PBE',\
                'structure':'fcc','element':'Pt','properties':'dB'}


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

print (code.value, exchange.value, struct.value, element.value, prop.value)

#Fig_canvas = gridplot([CF.p1, CF.p2, CF.p3, CF.p4])
controls1 = widgetbox([code, exchange, struct, element, prop, apply_crossfilter, apply_precision, clean_crossfilter],width=400)
                       #range_slider_lowK1, range_slider_medK1, range_slider_highK1], width=300)
controls2 = widgetbox([code2, exchange2, struct2, element2, prop2,apply_crossfilter2, apply_precision2, clean_crossfilter2],width=400)
                        #range_slider_lowK2, range_slider_medK2, range_slider_highK2, width=300)
controls3 = widgetbox([code3, exchange3, struct3, element3, prop3, apply_crossfilter3, apply_precision3, clean_crossfilter3], width=400)
                       #range_slider_lowK3, range_slider_medK3, range_slider_highK3], width=300)
controls4 = widgetbox([code4, exchange4, struct4, element4, prop4, apply_crossfilter4, apply_precision4, clean_crossfilter4], width=400)
                       #range_slider_lowK4, range_slider_medK4, range_slider_highK4], width=300)

layout_doc = layout([Desc_C1], [controls1, controls2, controls3, controls4], [CF1.p, CF2.p, CF3.p, CF4.p])#[CF1.p, CF2.p, CF3.p, CF4.p])#Desc_C1, controls1, Desc_C2, controls2,\
                    #Desc_C3, controls3, Desc_C4, controls_final)


print ('executed till here')

#z = Select(title='Z-Axis', value='None', options=plottables)
#z.on_change('value', update)
curdoc().add_root(layout_doc)
curdoc().title = "DFT Benchmark"

CF1.plot_prec_value1()
CF2.plot_prec_value2()
CF3.plot_prec_value3()
CF4.plot_prec_value4()
