import datetime
from ..core import db
import json
from bson import ObjectId

class Row(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    bz_integration = db.StringField()
    calculations_type = db.StringField()
    code = db.StringField()
    element = db.StringField()
    exchange = db.StringField()
    extrapolate = db.FloatField()
    extrapolate_err = db.FloatField()
    k_point = db.FloatField()
    pade_order = db.FloatField()
    perc_precisions = db.FloatField()
    precision = db.FloatField()
    properties = db.StringField()
    structure = db.StringField()
    #value = db.FloatField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {'bz_integration':self.bz_integration, 'calculations_type':self.calculations_type}
        data['code'] = self.code
        data['element'] = self.element
        data['exchange'] = self.exchange
        data['extrapolate'] = self.extrapolate
        data['extrapolate_err'] = self.extrapolate_err
        data['k-point'] = self.k_point
        data['pade_order'] = self.pade_order
        data['perc_precisions'] = self.perc_precisions
        data['precision'] = self.precision
        data['properties'] = self.properties
        data['structure'] = self.structure
        #data['value'] = self.value
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class RowEVK(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    code = db.StringField()
    element = db.StringField()
    structure = db.StringField()
    exchange = db.StringField()
    kpoints = db.FloatField()
    energy = db.FloatField()
    volume = db.FloatField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {}
        data['code'] = self.code
        data['element'] = self.element
        data['exchange'] = self.exchange
        data['structure'] = self.structure
        data['energy'] = self.energy
        data['volume'] = self.volume
        data['kpoints'] = self.kpoints
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class RowPade(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    code = db.StringField()
    element = db.StringField()
    structure = db.StringField()
    exchange = db.StringField()
    E0 = db.FloatField()
    E0_err = db.FloatField()
    V0 = db.FloatField()
    V0_err = db.FloatField()
    B = db.FloatField()
    B_err = db.FloatField()
    BP = db.FloatField()
    BP_err = db.FloatField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {}
        data['code'] = self.code
        data['element'] = self.element
        data['exchange'] = self.exchange
        data['structure'] = self.structure
        data['E0'] = self.E0
        data['E0_err'] = self.E0_err
        data['V0'] = self.V0
        data['V0_err'] = self.V0_err
        data['B'] = self.B
        data['B_err'] = self.B_err
        data['BP'] = self.BP
        data['BP_err'] = self.BP_err
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class RowPrecValue(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    code = db.StringField()
    element = db.StringField()
    structure = db.StringField()
    exchange = db.StringField()
    kpoints = db.FloatField()
    E0k = db.FloatField()
    V0k = db.FloatField()
    Bk = db.FloatField()
    BPk = db.FloatField()
    sE0k = db.FloatField()
    sV0k = db.FloatField()
    sBk = db.FloatField()
    sBPk = db.FloatField()

    def clone(self):
        del self.__dict__['_id']
        del self.__dict__['_created']
        del self.__dict__['_changed_fields']
        self.id = ObjectId()

    def info(self):
        data = {}
        data['code'] = self.code
        data['element'] = self.element
        data['exchange'] = self.exchange
        data['structure'] = self.structure
        data['kpoints'] = self.kpoints
        data['E0k'] = self.E0k
        data['V0k'] = self.V0k
        data['Bk'] = self.Bk
        data['BPk'] = self.BPk
        data['sE0k'] = self.sE0k
        data['sV0k'] = self.sV0k
        data['sBk'] = self.sBk
        data['sBPk'] = self.sBPk

        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
