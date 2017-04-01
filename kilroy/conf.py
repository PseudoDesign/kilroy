import yaml

class ConfigEntry:

    CONFIG_ENTRY_NAME = "MODULE_NAME"
    CONFIG_ENTRY_DATA = {
        "entry_type" : {
            "name" : CONFIG_ENTRY_NAME,
            "example_data_1" : "sample"
        }
    }

    @classmethod
    def get_example_config_string(cls, comment=False):
        retval = yaml.dump(cls.CONFIG_ENTRY_DATA, default_flow_style=False)
        if comment:
            retval = ("# " + retval.replace("\n", "\n# "))[:-2]
        return retval
