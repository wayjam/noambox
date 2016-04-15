import json
import inspect
'''
provide the method of converting between json and object
'''

class JSONObject:
    def __init__(self,d):
        self.__dict__ = d


def json2obj(j,o):
    json_obj2obj(json.load(j, object_hook= JSONObject),o)

def json_obj2obj(jo, oo):
    for k, v in vars(oo).items():
        if hasattr(jo,k):
            if inspect.isclass(v):
                json_obj2obj(jo.__dict__[k],oo.__dict__[k])
            else:
                setattr(oo, k, jo.__dict__[k])

def obj2json(data):
    return json.dumps(data, default=lambda o: o.__dict__,
                       indent=4)


def obj2jsons(f, content):
    json.dump(content, f, indent=4,
              default=lambda o: o.__dict__)
