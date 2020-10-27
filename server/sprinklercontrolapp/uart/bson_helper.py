import bson

def to_bson(obj):
    if obj.__dict__._state != None:
        return bson_from_model(obj)
    else:
        return bson.dumps(obj.__dict__)

def bson_from_model(model_instance):
    d = get_dict_except_state(model_instance)
    return bson.dumps(d)

def get_dict_except_state(obj):
    d = obj.__dict__
    return { k: d[k] for k in set(list(d.keys())) - set(['_state']) }

# What have you brought upon this cursed land!
"""
Create object from loaded dictionary:
class A:
    def __init__(self):
        self.x = 3


a1 = A()
a1.x = 2000
a1_bson = bson.dumps(a1.__dict__)

a2 = A()
print(a2.x)
> 3

bson_dict = bson.loads(a1_bson)
a2.__dict__.update(bson_dict)
print(a2.x)
> 2000

"""
