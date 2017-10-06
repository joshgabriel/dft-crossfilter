import requests
import json

def post_query(query_dict, endpoint):                                                  
    res = requests.post(url="http://0.0.0.0:6400/bench/v1/query_{}".\
          format(endpoint), data=json.dumps(query_dict))
    return res

def post_file(filename, endpoint):
    res = requests.post(url="http://0.0.0.0:6400/bench/v1/push/csv_{}".\
          format(endpoint), files= {'file':open(filename,'rb')})
    return res

if __name__ == '__main__':
    res_file = post_file(filename='../data/Data_Pade.csv',endpoint='extrapolate')
    print ('POSTED THE FILE!!!')
    res_query = post_query(query_dict={'code':'VASP','exchange':'PBE','element':'Al',\
                               'structure':'fcc'}, endpoint='extrapolate')
    print (res_query.content)
    print ('QUERIED SUCCESSFULLY!!')

