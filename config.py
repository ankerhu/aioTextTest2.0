import config_default
#支持x.y的dict
class Dict(dict):   
    def __init__(self,names=(),valuse=(),**kw):
        super(Dict,self).__init__(**kw)
        for k,v in zip(names,valuse):
            self[k] = v
    
    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s" % key)

    def __setattr__(self,key,value):
        self[key] = value

#递归
def merge(defaults,override):
    r = {}
    for k,v in defaults.items():
        if k in override:
            if isinstance(v,dict):
                r[k] = merge(v,override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

#递归
def toDict(d):
    D = Dict()
    for k,v in d.items():
        D[k] = toDict(v) if isinstance(v,dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs,config_override)
except ImportError:
    pass

configs = toDict(configs)