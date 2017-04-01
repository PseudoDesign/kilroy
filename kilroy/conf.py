import yaml

class ConfigEntry:

    CONFIG_ENTRY_NAME = "MODULE_NAME"
    CONFIG_ENTRY_DATA = {
        CONFIG_ENTRY_NAME : {
            "example_data_1" : "sample"
        }
    }

    @classmethod
    def get_example_config_string(cls, comment=False):
        retval = yaml.dump(cls.CONFIG_ENTRY_DATA, default_flow_style=False)
        if comment:
            retval = ("# " + retval.replace("\n", "\n# "))[:-2]
        return retval

    @classmethod
    def create_from_config_data(cls, data):
        return cls.create_from_kwargs(**data[cls.CONFIG_ENTRY_NAME])

    @classmethod
    def create_from_kwargs(cls, **kwargs):
        return ConfigEntry()
        

class Config:
    __entries = {}

    @classmethod
    def add_entry(cls, entry):
        if entry.CONFIG_ENTRY_NAME not in cls.__entries:
            cls.__entries[entry.CONFIG_ENTRY_NAME] = entry
        else:
            raise ValueError("Entry with key " + entry.key + " already exists")

    @classmethod
    def create_entry_from_yaml(cls, yaml_string):
        data = yaml.load(yaml_string)
        keys = data.keys()
        if len(keys) == 1 and list(keys)[0] in cls.__entries:
            return cls.__entries[list(keys)[0]].create_from_config_data(data)
        elif len(keys):
            raise ValueError("yaml_string was not properly formatted")
        else:
            raise ValueError(data.key + " is not a registered entry")
