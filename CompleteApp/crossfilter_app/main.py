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
from bokeh.sampledata.periodic_table import elements

import requests

plottables =  ['k-point', 'value', 'perc_precisions']

x_select = Select(title='X-Axis', value='k-point', options=plottables)

y_select = Select(title='Y-Axis', value='value', options=plottables)

############## Header Content from description.html  #################

content_filename1 = join(dirname(__file__), "ptable.html")

description1 = Div(text=open(content_filename1).read(),
                  render_as_text=False, width=600)

content_filename2 = join(dirname(__file__), "HomePage.html")

description2 = Div(text=open(content_filename2).read(),
                  render_as_text=False, width=600)

# periodic table widget
romans = ["I", "II", "III", "IV", "V", "VI", "VII"]

elements["atomic mass"] = elements["atomic mass"].astype(str)

print("Table---")
#print(elements.period)
print("---Table")

try:
  elements["period"] = [romans[x-1] for x in elements.period]
except:
  pass
elements = elements[elements.group != "-"]

group_range = [str(x) for x in range(1, 19)]


colormap = {
    "c"        : "#ffa07a",
    "nc"       : "#A9A9A9"
}

elems_colorpair = {'H':'nc','He':'nc',
                   'Li':'nc','Be':'nc','B':'nc','C':'nc', 'N':'nc', 'O':'nc','F':'nc','Ne':'nc',
                   'Na':'nc','Mg':'nc', 'Al':'c','Si':'nc','P':'nc','S':'nc','Cl':'nc','Ar':'nc',
                   'K': 'nc', 'Ca':'nc','Sc':'c', 'Ti':'c' ,'V':'c' , 'Cr':'c', 'Mn':'c', 'Fe':'c', 'Co':'c', 'Ni':'c', 'Cu':'c', 'Zn':'c',
                   'Rb':'nc', 'Sr':'nc','Y':'c', 'Zr':'c', 'Nb':'c', 'Mo':'c', 'Tc':'c', 'Ru':'c', 'Rh':'c', 'Pd':'c', 'Ag':'c','Cd': 'c',
                   'Cs':'nc', 'Ba':'nc', 'Hf':'c', 'Ta':'c', 'W':'c', 'Re':'c', 'Os':'c', 'Ir':'c', 'Pt':'c', 'Au':'c', 'Hg':'c'
                 }
elems_colorpair.update( { key:'nc' for key in list(elements['symbol']) if key not in list(elems_colorpair.keys()) } )

print ([ colormap[elems_colorpair[x]] for x in elements['symbol'] ])

source = ColumnDataSource(
    data=dict(
        group=[str(x) for x in elements["group"]],
        period=[str(y) for y in elements["period"]],
        symx=[str(x)+":0.1" for x in elements["group"]],
        numbery=[str(x)+":0.8" for x in elements["period"]],
        massy=[str(x)+":0.15" for x in elements["period"]],
        namey=[str(x)+":0.3" for x in elements["period"]],
        sym=elements["symbol"],
        name=elements["name"],
#        cpk=elements["CPK"],
        atomic_number=elements["atomic number"],
#        electronic=elements["electronic configuration"],
#        mass=elements["atomic mass"],
        B=['B' for x in elements["atomic mass"]],
        dB=['dB' for x in elements["atomic mass"]],
        V0=['V0' for x in elements["atomic mass"]],
        E0=['E0' for x in elements["atomic mass"]],
#        type=elements["metal"],
        type_color=[ colormap[elems_colorpair[x]] for x in elements['symbol'] ],
    )
)

# plot the periodic layout
#name = source.data["name"]
#B = source.data["B"]

# Display Table

#ptable1 = figure(title="Periodic Table", tools="hover",
#           x_range=group_range, y_range=list(reversed(romans)))

#ptable1.plot_width = 1500
#ptable1.toolbar_location = None
#ptable1.outline_line_color = None

#ptable1.background_fill_color = 'white'
#ptable1.rect("group", "period", 0.9, 0.9, source=source,
#       fill_alpha=0.3, color='type_color')

text_props = {
    "source": source,
    "angle": 0,
    "color": "black",
    "text_align": "left",
    "text_baseline": "middle"
}

#ptable1.text(x="symx", y="period", text="sym",
#       text_font_style="bold", text_font_size="22pt", **text_props)

#ptable1.text(x="symx", y="numbery", text="atomic_number",
#       text_font_size="9pt", **text_props)

#ptable1.grid.grid_line_color = None


#ptable1.select_one(HoverTool).tooltips = [
#    ("name", "@name"),
#    ("V0 (A^3 per atom)", "@V0"),
#    ("B (GPa)", "@B"),
#    ("dB/dP", "@dB")
#]

#Interactive table

ptable2 = figure(title="Periodic Table", tools="hover",
           x_range=group_range, y_range=list(reversed(romans)))

ptable2.plot_width = 1500
ptable2.toolbar_location = None
ptable2.outline_line_color = None

ptable2.background_fill_color = 'white'
ptable2.rect("group", "period", 0.9, 0.9, source=source,
       fill_alpha=0.3, color='type_color')

ptable2.text(x="symx", y="period", text="sym",
       text_font_style="bold", text_font_size="22pt", **text_props)

ptable2.text(x="symx", y="numbery", text="atomic_number",
       text_font_size="9pt", **text_props)

ptable2.grid.grid_line_color = None


ptable2.select_one(HoverTool).tooltips = [
    ("name", "@name"),
    ("V0 (A^3 per atom)", "@V0"),
    ("B (GPa)", "@B"),
    ("dB/dP", "@dB")
]

######### CREATES CROSSFILTER ##########################


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


    def update_ptable(self):
        """
        update the periodic table highlighted elements
        """
        from bokeh.sampledata.periodic_table import elements
        romans = ["I", "II", "III", "IV", "V", "VI", "VII"]

        elements["atomic mass"] = elements["atomic mass"].astype(str)

        elements["period"] = [x for x in elements.period]
        elements = elements[elements.group != "-"]

        group_range = [str(x) for x in range(1, 19)]
        print ('reaches colormap def')
        colormap = {
                     "c"        : "#ffa07a",
                     "nc"       : "#A9A9A9"
                   }
        elems_colorpair = {}

        fcc_B_extrapol_props = {}
        fcc_dB_extrapol_props = {}
        fcc_V0_extrapol_props = {}
        fcc_E0_extrapol_props = {}

        bcc_B_extrapol_props = {}
        bcc_dB_extrapol_props = {}
        bcc_V0_extrapol_props = {}
        bcc_E0_extrapol_props = {}

        hcp_B_extrapol_props = {}
        hcp_dB_extrapol_props = {}
        hcp_V0_extrapol_props = {}
        hcp_E0_extrapol_props = {}

        available_elems = []

        for e in elements["symbol"]:
          if e in np.unique(list(self.plot_data['element'])):
              available_elems.append(e)
              for s in np.unique(list(self.plot_data['structure'])):
                plot_struct = self.plot_data[self.plot_data['structure']==s]
                plot_struct_elem = plot_struct[plot_struct['element']==e]
                if s=='fcc':
                     try:
                         fcc_B_extrapol_props.update({e:list(plot_struct_elem['B'])[0]})

                         fcc_dB_extrapol_props.update({e:list(plot_struct_elem['BP'])[0]})

                         fcc_V0_extrapol_props.update({e:list(plot_struct_elem['V0'])[0]})

                         fcc_E0_extrapol_props.update({e:list(plot_struct_elem['E0'])[0]})
                     except:
                         pass
                elif s=='bcc':
                     try:
                         bcc_B_extrapol_props.update({e:list(plot_struct_elem['B'])[0]})

                         bcc_dB_extrapol_props.update({e:list(plot_struct_elem['BP'])[0]})

                         bcc_V0_extrapol_props.update({e:list(plot_struct_elem['V0'])[0]})

                         bcc_E0_extrapol_props.update({e:list(plot_struct_elem['E0'])[0]})
                     except:
                         pass
                elif s=='hcp':
                     try:
                         hcp_B_extrapol_props.update({e:list(plot_struct_elem['B'])[0]})

                         hcp_dB_extrapol_props.update({e:list(plot_struct_elem['BP'])[0]})

                         hcp_V0_extrapol_props.update({e:list(plot_struct_elem['V0'])[0]})

                         hcp_E0_extrapol_props.update({e:list(plot_struct_elem['E0'])[0]})
                     except:
                        pass
        fcc_E0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in fcc_E0_extrapol_props})
        fcc_V0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in fcc_V0_extrapol_props})
        fcc_B_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in fcc_B_extrapol_props})
        fcc_dB_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in fcc_dB_extrapol_props})

        bcc_E0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in bcc_E0_extrapol_props})
        bcc_V0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in bcc_V0_extrapol_props})
        bcc_B_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in bcc_B_extrapol_props})
        bcc_dB_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in bcc_dB_extrapol_props})

        hcp_E0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in hcp_E0_extrapol_props})
        hcp_V0_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in hcp_V0_extrapol_props})
        hcp_B_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in hcp_B_extrapol_props})
        hcp_dB_extrapol_props.update({k:'xxx' for k in elements['symbol'] if k not in hcp_dB_extrapol_props})

        elems_colorpair.update( { key:'c' for key in np.unique(available_elems) } )
        elems_colorpair.update( { key:'nc' for key in list(elements['symbol']) if key not in list(elems_colorpair.keys()) } )


        print ([ colormap[elems_colorpair[x]] for x in elements['symbol'] ])

        source = ColumnDataSource(
              data=dict(
                     group=[str(x) for x in elements["group"]],
                     period=[str(y) for y in elements["period"]],
                     symx=[str(x)+":0.1" for x in elements["group"]],
                     numbery=[str(x)+":0.8" for x in elements["period"]],
                     massy=[str(x)+":0.15" for x in elements["period"]],
                     namey=[str(x)+":0.3" for x in elements["period"]],
                     sym=elements["symbol"],
                     name=elements["name"],
#                     cpk=elements["CPK"],
                     atomic_number=elements["atomic number"],
#                     electronic=elements["electronic configuration"],
                     fcc_B=[fcc_B_extrapol_props[x] for x in elements["symbol"]],
                     fcc_dB=[fcc_dB_extrapol_props[x] for x in elements["symbol"]],
                     fcc_V0=[fcc_V0_extrapol_props[x] for x in elements["symbol"]],
                     fcc_E0=[fcc_E0_extrapol_props[x] for x in elements["symbol"]],
                     bcc_B=[bcc_B_extrapol_props[x] for x in elements["symbol"]],
                     bcc_dB=[bcc_dB_extrapol_props[x] for x in elements["symbol"]],
                     bcc_V0=[bcc_V0_extrapol_props[x] for x in elements["symbol"]],
                     bcc_E0=[bcc_E0_extrapol_props[x] for x in elements["symbol"]],
                     hcp_B=[hcp_B_extrapol_props[x] for x in elements["symbol"]],
                     hcp_dB=[hcp_dB_extrapol_props[x] for x in elements["symbol"]],
                     hcp_V0=[hcp_V0_extrapol_props[x] for x in elements["symbol"]],
                     hcp_E0=[hcp_E0_extrapol_props[x] for x in elements["symbol"]],
                     type=elements["metal"],
                     type_color=[ colormap[elems_colorpair[x]] for x in elements['symbol'] ],
                      )
                                 )

        # plot the periodic layout
        #name = source.data["name"]
        #B = source.data["B"]

        ptable = figure(title="Periodic Table", tools="hover",
           x_range=group_range, y_range=list(reversed(romans)))
        ptable.background_fill_color='white'
        ptable.plot_width = 1500
        ptable.toolbar_location = None
        ptable.outline_line_color = None

        ptable.rect("group", "period", 0.9, 0.9, source=source,
                    fill_alpha=0.3, color='type_color')

        text_props = {
           "source": source,
           "angle": 0,
           "color": "black",
           "text_align": "left",
           "text_baseline": "middle"
                     }

        ptable.text(x="symx", y="period", text="sym",
        text_font_style="bold", text_font_size="22pt", **text_props)

        ptable.text(x="symx", y="numbery", text="atomic_number",
        text_font_size="9pt", **text_props)

#        ptable.text(x="symx", y="namey", text="name",
#        text_font_size="6pt", **text_props)

#        ptable.text(x="symx", y="massy", text="mass",
#        text_font_size="5pt", **text_props)

        ptable.grid.grid_line_color = None


        ptable.select_one(HoverTool).tooltips = [
        ("name", "@name"),
        ("fcc, V0 (A^3 per atom)", "@fcc_V0"),
        ("fcc, B (GPa)", "@fcc_B"),
        ("fcc, dB/dP", "@fcc_dB"),
        ("bcc, V0 (A^3 per atom)", "@bcc_V0"),
        ("bcc, B (GPa)", "@bcc_B"),
        ("bcc, dB/dP", "@bcc_dB"),
        ("hcp, V0 (A^3 per atom)", "@hcp_V0"),
        ("hcp, B (GPa)", "@hcp_B"),
        ("hcp, dB/dP", "@hcp_dB")]
        return ptable

    def convert_multi_query_to_dicts(self,user_query):
        """
        """
        for k in user_query:
            self.query_api(endpoint='precvalue')
        pass

    def plot_prec_value(self):
       print ('Triggering crossfilter')
       print ('executes this on startup')
       layout.children[6] = self.multi_2Dplot_pade_figure(self.plot_data)

    def multi_2Dplot_pade_figure(self,datasets):
        """
        method which plots multiple curves of different color
        on the same bokeh figure canvas. Will receive query results from the precvalue
        end point on the E0k, V0k, Bk, BPk, kpoints data. x is always kpoints data log scaled

        Example user query is {'code':'VASP','exchange':'PBE','element':'Al','structure':'fcc','property':'B'} +
                              {'code':'VASP','exchange':'PBE','element':'Al','structure':'hcp','property':'B'} +
                              {'code':'DMol3','exchange':'LDA','element':'Al','structure':'fcc', 'property':'B'} +
                              {'code':'DMol3','exchange':'LDA','element':'Al','structure':'hcp', 'property':'B'}
        """
        # receive a dict of datasets: {'Plot1':{'x':[],'y':[], 'x_title': None, 'y_title': None,
        # 'Characteristic':'VASP_PBE_Al_fcc_B'}, 'Plot2':{'x':[],'y':[], 'x_title': None, 'y_title': None}}

        def color_marker_divider(characteristics):
            cm_keys= {'00':('red','*'),'01':('red','-.-'),'02':('red','*'),'03':('red','^'),\
             '10':('blue','*'),'11':('blue','-.-'),'12':('blue','*'),'13':('blue','^')
             }
            DictCharacters = \
            [{n:att for n,att in enumerate(c.split('_'))} for c in characteristics]
            # one or two char value different and same code and exchange: same color different marker
            # else different color and marker.
            return cm_keys
        kw = {}
        kw['title'] = 'Pade Analysis Plots'
        kw['x_axis_type'] = 'log'
        self.p1 = figure(plot_height=600, plot_width=800, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)

        self.p1.xaxis.axis_label = x_title
        self.p1.yaxis.axis_label = y_title
        #color_marker_divider(characteristics)
        for dset in datasets:
            xs = datasets[dset]['x']
            ys = datasets[dset]['y']
            #c,m = color_marker_divider(characteristics)['00']
            self.p1.scatter(x=xs, y=ys)#, alpha=1.0, hover_color='blue', hover_alpha=1.0)
        return self.p1

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
       layout.children[1] =  self.update_ptable()
       print ('finished callback to update layout')

    def update_prop(self):
       self.query_dict.update({'properties':prop.value})

    def update_kpoints(self):
        pass

    def update_x(self):
        self.x = x.value
        pass

    def update_y(self):
        self.y = y.value
        pass

    def query_api(self,endpoint):
        r = requests.post(url='http://www.dftbenchmarkmgi.com:7200/bench/v1/query_{}'.\
                          format(endpoint),data=json.dumps(self.query_dict))
        ListOfDicts = r.json()['content']
        self.plot_data = pd.concat([pd.DataFrame({k:[ld[k]] for k in list(ld.keys())}) for ld in ListOfDicts])



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

CF = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE'})

# first query for the periodic table data
CF.query_api(endpoint='extrapolate')
print (CF.plot_data)

# for the first table to display VASP PBE all structures Pade extrapolates for all properties
# as a bonus with some error bar too

ptable1 = CF.update_ptable()

layout_doc = column(description1, ptable1, description2)

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

print ('executed till here')

curdoc().add_root(layout_doc)
curdoc().title = "DFT Benchmark"
update()
