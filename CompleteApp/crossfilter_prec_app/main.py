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
from precision.precisions import DatabaseData

import requests

plottables =  ['k-point', 'value', 'perc_precisions']

x_select = Select(title='X-Axis', value='k-point', options=plottables)

y_select = Select(title='Y-Axis', value='value', options=plottables)

############## Header Content from description.html  #################

content_filename1 = join(dirname(__file__), "ptable.html")

description1 = Div(text=open(content_filename1).read(),
                  render_as_text=False, width=600)

content_filename2 = join(dirname(__file__), "UserInstructions.html")

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

    def query_ptable_api(self,endpoint):
        r = requests.post(url='http://0.0.0.0:6400/bench/v1/query_{}'.\
                          format(endpoint),data=json.dumps(self.query_dict))
        ListOfDicts = r.json()['content']
        self.plot_data = pd.concat([pd.DataFrame({k:[ld[k]] for k in list(ld.keys())}) for ld in ListOfDicts])


    def query_api(self,endpoint):
        query_dict ={k:v for k,v in self.query_dict.items() if k!='properties'}
        self.properties = self.query_dict['properties']
        if self.properties == 'dB':
            self.properties = 'BP'
        r = requests.post(url='http://0.0.0.0:6400/bench/v1/query_{}'.\
                          format(endpoint),data=json.dumps(self.query_dict))
        ListOfDicts = r.json()['content']
        self.plot_data = pd.concat([pd.DataFrame({k:[ld[k]] for k in list(ld.keys())}) for ld in ListOfDicts])


    def create_figure_new(self):
        """
        create a new multi-figure canvas
        """
        kw = {}
        self.p = figure(plot_height=400, plot_width=400, tools='pan,wheel_zoom,box_zoom,reset,hover', **kw)
        self.p.circle(x=[0],y=[0])


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

       layout_doc.children[4].children[0] = self.plot_pade_figure()

    def clear_crossfilter1(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[4].children[0] = self.p

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

       layout_doc.children[4].children[1] = self.plot_pade_figure()

    def clear_crossfilter2(self):
        """
        clear the figure and crossfilter
        """
        print ('Trigger clear')
        self.query_dict = {}
        self.plot_data = None
        self.create_figure_new()
        layout_doc.children[4].children[1] = self.p


    def plot_pade_figure(self):
        """
        method which plots multiple curves of different color
        on the same bokeh figure canvas. Will receive query results from the evk
        end point on the E0k, V0k, Bk, BPk, kpoints data. x is always kpoints data log scaled
        """
        data_analysis = DatabaseData(dataframe=self.plot_data)
        print (data_analysis.dataframe.columns)
        data_analysis.run_pade_through_R(rscript='birch',get_inits_ev=True)
        data_analysis.create_precisions()
        data_analysis.extract_pade_curve()
        x_eos_kpts, y_eos, xs_err, ys_err, x_pade_kpts, y_pade = \
        data_analysis.create_pade_bokeh_compat(properties=self.properties)
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
        if self.properties == 'B':
            p.yaxis.axis_label = 'Bulk Modulus B (GPa)'
        elif self.properties == 'dB':
            p.yaxis.axis_label = 'Bulk Modulus Pressure Derivative'
        elif self.properties == 'E0':
            p.yaxis.axis_label = 'DFT Energy (eV/atom)'
        elif self.properties == 'V0':
            p.yaxis.axis_label = 'Volume (A^3/atom)'

        return p

    def plot_precision_figure(self):
        """
        method which plots multiple curves of different color
        on the same bokeh figure canvas. Will receive query results from the evk
        end point on the E0k, V0k, Bk, BPk, kpoints data. x is always kpoints data log scaled
        """

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
                        'structure':struct.value,'element':element.value,'properties':prop.value}
        print ('POSTING', self.query_dict)
        if not self.query_dict['properties'] == 'Multi':
            self.query_api(endpoint='precvalue')
            self.prop_data = self.plot_data['s{}k'.format(self.properties)]
            self.energy_data = self.plot_data['sE0k'.format(self.properties)]

        layout_doc.children[4].children[0] = self.plot_precision_figure()
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
        layout_doc.children[4].children[1] = self.plot_precision_figure()



## PTABLE


CF = CrossFiltDFs(query_dict={'code':'VASP','exchange':'PBE'})

# first query for the periodic table data
CF.query_ptable_api(endpoint='extrapolate')
print (CF.plot_data)

# for the first table to display VASP PBE all structures Pade extrapolates for all properties
# as a bonus with some error bar too

ptable1 = CF.update_ptable()


## PLOT 1

CF1 = CrossFiltDFs()

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




## PLOT 2


CF2 = CrossFiltDFs()

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




CF1.create_figure_new()
CF2.create_figure_new()



controls1 = widgetbox([code, exchange, struct, element, prop, apply_crossfilter, apply_precision, clean_crossfilter],width=400)
                       #range_slider_lowK1, range_slider_medK1, range_slider_highK1], width=300)
controls2 = widgetbox([code2, exchange2, struct2, element2, prop2,apply_crossfilter2, apply_precision2, clean_crossfilter2],width=400)
                        #range_slider_lowK2, range_slider_medK2, range_slider_highK2, width=300)



#layout_doc = column(description1, ptable1, description2)

layout_doc = layout([description1],[ptable1],[description2],[controls1, controls2], [CF1.p, CF2.p])

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

CF1.plot_prec_value1()
CF2.plot_prec_value2()

