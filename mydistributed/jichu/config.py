# 程序是把所有的config_default里的文件配置成override的
from mydistributed.jichu import config_default

configs = config_default.configs


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


try:
    import config_override

    configs = merge(configs, config_override.configs)
    print(configs)
except ImportError:
    pass
