import yaml


class ConfigEntry:

    CONFIG_ENTRY_NAME = "MODULE_NAME"
    CONFIG_ENTRY_DATA = {
        CONFIG_ENTRY_NAME : {
            "example_data_1" : "sample"
        }
    }

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_example_config_string(cls, comment=False):
        retval = yaml.dump(cls.CONFIG_ENTRY_DATA, default_flow_style=False)
        if comment:
            retval = ("# " + retval.replace("\n", "\n# "))[:-2]
        return retval

    @classmethod
    def create_from_config_data(cls, data):
        return cls(**data)


class Config:
    __entries = {}

    def __init__(self):
        pass

    @classmethod
    def add_entry(cls, entry):
        if entry.CONFIG_ENTRY_NAME not in cls.__entries:
            cls.__entries[entry.CONFIG_ENTRY_NAME] = entry
        else:
            raise ValueError(
                "Entry with key " + entry.CONFIG_ENTRY_NAME + " already exists"
                )

    @classmethod
    def create_entry(cls, name, data):
        if name in cls.__entries:
            return cls.__entries[name].create_from_config_data(data)
        else:
            raise ValueError(name + " is not a registered entry")
