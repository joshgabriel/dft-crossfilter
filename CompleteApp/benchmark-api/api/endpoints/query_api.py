import json

from flask.ext.api import status
import flask as fk

from api import app, API_URL, crossdomain, api_response
from benchdb.common.models.row_model import Row, RowEVK, RowPade, RowPrecValue
from benchdb.common.models import Attribute

import mimetypes
import json
import traceback
import datetime
import random
import string
import os
from io import BytesIO
import pandas as pd
import tempfile

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

@app.route(API_URL + '/push/csv_evk', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def home_evk_data():
    if fk.request.method == 'POST':
        if fk.request.files:
            file_obj = fk.request.files['file']
            file_name = file_obj.filename
            print (file_name)
            dataObject = BytesIO()

            #head = Row.objects(index='0').first()

            tmp_csv = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            content = file_obj.read().decode("UTF8")
            tmp_csv.write(str(content))
            csv_path = tmp_csv.name
            data = None

            data = pd.read_csv(str(csv_path))
            # print(data)
            print("Read in pandas")

            #if head == None:
            head = RowEVK(index='0')
            head.value = [ col for col in data.columns if col != 'Unnamed: 0']
            print (head.value)
            head.save()
            print("Head done.")

            print("Head section loaded...")
            header = ','.join(head.value)
            print('%s\n'%header)
            dataObject.write(str('%s\n'%header).encode("utf-8"))
            print("Head written to dataframe...")

            previous_index = len(RowEVK.objects())

            for index, row in data.iterrows():
                rw = RowEVK(created_at = datetime.datetime.utcnow(),\
                    code = str(row['code']),\
                    element = str(row['element']),\
                    exchange = str(row['exchange']),\
                    structure = str(row['structure']),\
                    energy = float(row['energy']),\
                    volume = float(row['volume']),\
                    kpoints = float(row['kpoints']))
                rw.save()
                oneline = ','.join([str(rw._data[k]) for k in list(rw._data.keys())])
                print (oneline)
                dataObject.write(str('%s\n'%oneline).encode("utf-8"))


            print("New data appended to old data...")

            dataObject.seek(0)
            data_merged = pd.read_csv(dataObject)

            return api_response(200, 'Push succeed', 'Your file was pushed.')
        else:
            return api_response(204, 'Nothing created', 'You must a set file.')

    return """
    <!doctype html>
    <html>
        <head>
          <!-- css  -->
          <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
          <link href="http://0.0.0.0:4000/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
          <link href="http://0.0.0.0:4000/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>

          <!--Let browser know website is optimized for mobile-->
          <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
          <title>Benchmark Platform</title>
        </head>
        <body>
            <nav class="white" role="navigation">
                <div class="nav-wrapper container">
                  <a id="logo-container" href="http://0.0.0.0:8000" class="teal-text text-lighten-2">Reference</a>
                </div>
            </nav>
            <div class="valign center-align">
                <h1>Upload dataset</h1>
                <form action="" method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
            <!--Import jQuery before materialize.js-->
            <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
            <script type="text/javascript" src="http://0.0.0.0:4000/js/materialize.min.js"></script>
        </body>
    </html>
    """

@app.route(API_URL + '/push/csv_precvalue', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def home_precvalue_data():
    if fk.request.method == 'POST':
        if fk.request.files:
            file_obj = fk.request.files['file']
            file_name = file_obj.filename
            print (file_name)
            dataObject = BytesIO()

            #head = Row.objects(index='0').first()

            tmp_csv = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            content = file_obj.read().decode("UTF8")
            tmp_csv.write(str(content))
            csv_path = tmp_csv.name
            data = None

            data = pd.read_csv(str(csv_path))
            # print(data)
            print("Read in pandas")

            #if head == None:
            head = RowPrecValue(index='0')
            head.value = [ col for col in data.columns if col != 'Unnamed: 0']
            print (head.value)
            head.save()
            print("Head done.")

            print("Head section loaded...")
            header = ','.join(head.value)
            print('%s\n'%header)
            dataObject.write(str('%s\n'%header).encode("utf-8"))
            print("Head written to dataframe...")

            previous_index = len(RowPrecValue.objects())

            for index, row in data.iterrows():
                rw = RowPrecValue(created_at = datetime.datetime.utcnow(),\
                    code = str(row['code']),\
                    element = str(row['element']),\
                    exchange = str(row['exchange']),\
                    structure = str(row['structure']),\
                    E0k = float(row['E0k']),\
                    V0k = float(row['V0k']),\
                    Bk = float(row['Bk']),\
                    BPk = float(row['BPk']),\
                    sE0k = float(row['sE0k']),\
                    sV0k = float(row['sV0k']),\
                    sBk = float(row['sBk']),\
                    sBPk = float(row['sBPk']),\
                    kpoints = float(row['kpoints']))
                rw.save()
                oneline = ','.join([str(rw._data[k]) for k in list(rw._data.keys())])
                print (oneline)
                dataObject.write(str('%s\n'%oneline).encode("utf-8"))


            print("New data appended to old data...")

            dataObject.seek(0)
            data_merged = pd.read_csv(dataObject)

            return api_response(200, 'Push succeed', 'Your file was pushed.')
        else:
            return api_response(204, 'Nothing created', 'You must a set file.')

    return """
    <!doctype html>
    <html>
        <head>
          <!-- css  -->
          <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
          <link href="http://0.0.0.0:4000/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
          <link href="http://0.0.0.0:4000/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>

          <!--Let browser know website is optimized for mobile-->
          <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
          <title>Benchmark Platform</title>
        </head>
        <body>
            <nav class="white" role="navigation">
                <div class="nav-wrapper container">
                  <a id="logo-container" href="http://0.0.0.0:8000" class="teal-text text-lighten-2">Reference</a>
                </div>
            </nav>
            <div class="valign center-align">
                <h1>Upload dataset</h1>
                <form action="" method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
            <!--Import jQuery before materialize.js-->
            <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
            <script type="text/javascript" src="http://0.0.0.0:4000/js/materialize.min.js"></script>
        </body>
    </html>
    """


@app.route(API_URL + '/push/csv_extrapolate', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def home_extrapolate_data():
    if fk.request.method == 'POST':
        if fk.request.files:
            file_obj = fk.request.files['file']
            file_name = file_obj.filename
            print (file_name)
            dataObject = BytesIO()
            tmp_csv = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            content = file_obj.read().decode("UTF8")
            tmp_csv.write(str(content))
            csv_path = tmp_csv.name
            data = None

            data = pd.read_csv(str(csv_path))
            print("Read in pandas")

            head = RowPade(index='0')
            head.value = [ col for col in data.columns if col != 'Unnamed: 0']
            print (head.value)
            head.save()
            print("Head done.")

            print("Head section loaded...")
            header = ','.join(head.value)
            print('%s\n'%header)
            dataObject.write(str('%s\n'%header).encode("utf-8"))
            print("Head written to dataframe...")

            previous_index = len(RowPade.objects())

            for index, row in data.iterrows():
                rw = RowPade(created_at = datetime.datetime.utcnow(),\
                    code = str(row['code']),\
                    element = str(row['element']),\
                    exchange = str(row['exchange']),\
                    structure = str(row['structure']),\
                    E0 = float(row['E0']),\
                    E0_err = float(row['E0_err']),\
                    V0 = float(row['V0']),\
                    V0_err = float(row['V0_err']),\
                    B = float(row['B']),\
                    B_err = float(row['B_err']),\
                    BP = float(row['BP']),\
                    BP_err = float(row['BP_err']))
                rw.save()
                oneline = ','.join([str(rw._data[k]) for k in list(rw._data.keys())])
                print (oneline)
                dataObject.write(str('%s\n'%oneline).encode("utf-8"))

            print("New data appended to old data...")

            return api_response(200, 'Push succeed', 'Your file was pushed.')
        else:
            return api_response(204, 'Nothing created', 'You must a set file.')

    return """
    <!doctype html>
    <html>
        <head>
          <!-- css  -->
          <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
          <link href="http://0.0.0.0:4000/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
          <link href="http://0.0.0.0:4000/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>

          <!--Let browser know website is optimized for mobile-->
          <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
          <title>Benchmark Platform</title>
        </head>
        <body>
            <nav class="white" role="navigation">
                <div class="nav-wrapper container">
                  <a id="logo-container" href="http://0.0.0.0:8000" class="teal-text text-lighten-2">Reference</a>
                </div>
            </nav>
            <div class="valign center-align">
                <h1>Upload dataset</h1>
                <form action="" method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
            <!--Import jQuery before materialize.js-->
            <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
            <script type="text/javascript" src="http://0.0.0.0:4000/js/materialize.min.js"></script>
        </body>
    </html>
    """

@app.route(API_URL + '/push/csv_experimental_ref', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def home_experiment_data():
    if fk.request.method == 'POST':
        if fk.request.files:
            file_obj = fk.request.files['file']
            file_name = file_obj.filename
            print (file_name)
            dataObject = BytesIO()

            tmp_csv = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            content = file_obj.read().decode("UTF8")
            tmp_csv.write(str(content))
            csv_path = tmp_csv.name
            data = None

            data = pd.read_csv(str(csv_path))
            # print(data)
            print("Read in pandas")

            head = Row(index='0')
            head.value = [ col for col in data.columns if col != 'Unnamed: 0']
            print (head.value)
            head.save()
            print("Head done.")

            print("Head section loaded...")
            header = ','.join(head.value)
            print('%s\n'%header)
            dataObject.write(str('%s\n'%header).encode("utf-8"))
            print("Head written to dataframe...")

            previous_index = len(Row.objects())

            for index, row in data.iterrows():
                rw = Row(created_at = datetime.datetime.utcnow(),\
                    bz_integration = str(row['bz_integration']),\
                    calculations_type = str(row['calculations_type']),\
                    code = str(row['code']),\
                    element = str(row['element']),\
                    exchange = str(row['exchange']),\
                    extrapolate = float(row['extrapolate']),\
                    extrapolate_err = float(row['extrapolate_err']),\
                    k_point = float(row['k-point']),\
                    pade_order = float(row['pade_order']),\
                    perc_precisions = float(row['perc_precisions']),\
                    precision = float(row['precision']),\
                    properties = str(row['properties']),\
                    structure = str(row['structure']))
                rw.save()
                oneline = ','.join([str(rw._data[k]) for k in list(rw._data.keys())])
                print (oneline)
                dataObject.write(str('%s\n'%oneline).encode("utf-8"))

            print("New data appended to old data...")
            return api_response(200, 'Push succeed', 'Your file was pushed.')

        else:
            return api_response(204, 'Nothing created', 'You must a set file.')

    return """
    <!doctype html>
    <html>
        <head>
          <!-- css  -->
          <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
          <link href="http://0.0.0.0:4000/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
          <link href="http://0.0.0.0:4000/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>

          <!--Let browser know website is optimized for mobile-->
          <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
          <title>Benchmark Platform</title>
        </head>
        <body>
            <nav class="white" role="navigation">
                <div class="nav-wrapper container">
                  <a id="logo-container" href="http://0.0.0.0:8000" class="teal-text text-lighten-2">Reference</a>
                </div>
            </nav>
            <div class="valign center-align">
                <h1>Upload dataset</h1>
                <form action="" method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
            <!--Import jQuery before materialize.js-->
            <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
            <script type="text/javascript" src="http://0.0.0.0:4000/js/materialize.min.js"></script>
        </body>
    </html>
    """

@app.route(API_URL + '/desc/all', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_desc_all():
    if fk.request.method == 'GET':
        _descriptions = DescModel.objects()
        descriptions = []
        for desc in _descriptions:
            descriptions.append(desc.info())
        return api_response(200, 'Columns descriptions', descriptions)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/desc/single/<column>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_desc_single(column):
    if fk.request.method == 'GET':
        description = DescModel.objects(column=column).first()
        if description:
            return api_response(200, 'Column [%s] description'%column, description.df)
        else:
            return api_response(204, 'Nothing found', "No column with that name.")
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')


@app.route(API_URL + '/clear', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def clear():
    if fk.request.method == 'GET':
        descriptions = DescModel.objects()
        for desc in descriptions:
            desc.delete()
        cols = ColModel.objects()
        for col in cols:
            col.delete()
        rws = RowModel.objects()
        for rw in rws:
            rw.delete()
        return api_response(204, 'Clear done', "Everything is wiped out.")
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/col/all', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_col_all():
    if fk.request.method == 'GET':
        _cols = ColModel.objects()
        cols = []
        for col in _cols:
            cols.append(col.info())
        return api_response(200, 'Columns values', cols)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/col/dict/all', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_col_dict_all():
    if fk.request.method == 'GET':
        _cols = ColModel.objects()
        cols = {}
        for col in _cols:
            info = col.info()
            cols[col.column] = col.values
        return api_response(200, 'Columns as dicts', cols)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/col/dict/bare', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_col_dict_bare():
    if fk.request.method == 'GET':
        _cols = ColModel.objects()
        cols = {}
        for col in _cols:
            info = col.info()
            cols[col.column] = []
        return api_response(200, 'Columns as bare dicts', cols)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/col/single/<column>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_single_single(column):
    if fk.request.method == 'GET':
        col = ColModel.objects(column=column).first()
        if col:
            return api_response(200, 'Column [%s] content'%column, col.info())
        else:
            return api_response(204, 'Nothing found', "No column with that name.")
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/row/all', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_row_all():
    if fk.request.method == 'GET':
        _rws = Row.objects()
        rws = []
        for rw in _rws:
            rws.append(rw.info())
        return api_response(200, 'Rows values', rws)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/attributes', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def attributes():
    if fk.request.method == 'GET':
        attrs = Attribute.objects()
        data = {}
        for attr in attrs:
            data[attr.name] = attr.values
        return api_response(200, 'Overall attributes', data)
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/query', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_row():
    if fk.request.method == 'POST':
        if fk.request.data:
            print ('comes here with {}'.format(fk.request.data))
            data = json.loads(fk.request.data)
            code = data.get("code", None)
            exchange = data.get("exchange", None)
            structure = data.get("structure", None)
            element = data.get("element", None)
            property = data.get("property", None)
            data = []
            for row in Row.objects:
                include = True
                if code:
                    include = include & (row.code == code)
                if exchange:
                    include = include & (row.exchange == exchange)
                if structure:
                    include = include & (row.structure == structure)
                if element:
                    include = include & (row.element == element)
                if property:
                    include = include & (row.property == property)
                if include:
                    data.append(row.info())
            return api_response(200, 'Filtered rows', data)
        else:
            print ('does not go there')
            return api_response(200, 'All rows', [row.info() for row in Row.objects()])
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')


@app.route(API_URL + '/query_evk', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_evk():
    if fk.request.method == 'POST':
        if fk.request.data:
            print ('comes here with {}'.format(fk.request.data))
            data = json.loads(fk.request.data)
            code = data.get("code", None)
            exchange = data.get("exchange", None)
            structure = data.get("structure", None)
            element = data.get("element", None)
            data = []
            for row in RowEVK.objects:
                include = True
                if code:
                    include = include & (row.code == code)
                if exchange:
                    include = include & (row.exchange == exchange)
                if structure:
                    include = include & (row.structure == structure)
                if element:
                    include = include & (row.element == element)
                if include:
                    data.append(row.info())
            return api_response(200, 'Filtered rows', data)
        else:
            print ('does not go there')
            return api_response(200, 'All rows', [row.info() for row in Row.objects()])
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/query_extrapolate', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_extrapolate():
    if fk.request.method == 'POST':
        if fk.request.data:
            print ('comes here with {}'.format(fk.request.data))
            data = json.loads(fk.request.data)
            code = data.get("code", None)
            exchange = data.get("exchange", None)
            structure = data.get("structure", None)
            element = data.get("element", None)
            data = []
            for row in RowPade.objects:
                include = True
                if code:
                    include = include & (row.code == code)
                if exchange:
                    include = include & (row.exchange == exchange)
                if structure:
                    include = include & (row.structure == structure)
                if element:
                    include = include & (row.element == element)
                if include:
                    data.append(row.info())
            return api_response(200, 'Filtered rows', data)
        else:
            print ('does not go there')
            return api_response(200, 'All rows', [row.info() for row in Row.objects()])
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(API_URL + '/query_precvalue', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(origin='*')
def query_precvalue():
    if fk.request.method == 'POST':
        if fk.request.data:
            print ('comes here with {}'.format(fk.request.data))
            data = json.loads(fk.request.data)
            code = data.get("code", None)
            exchange = data.get("exchange", None)
            structure = data.get("structure", None)
            element = data.get("element", None)
            kpoint = data.get("k-point",None)
            data = []
            for row in RowPrecValue.objects:
                include = True
                if code:
                    include = include & (row.code == code)
                if exchange:
                    include = include & (row.exchange == exchange)
                if structure:
                    include = include & (row.structure == structure)
                if element:
                    include = include & (row.element == element)
                if include:
                    data.append(row.info())
            return api_response(200, 'Filtered rows', data)
        else:
            print ('does not go there')
            return api_response(200, 'All rows', [row.info() for row in Row.objects()])
    else:
        return api_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
