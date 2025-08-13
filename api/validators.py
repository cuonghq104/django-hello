from django.utils.module_loading import import_string
from django.conf import settings

def load_validators(setting_name):
    validators = []
    for v in getattr(settings, setting_name, []):
        cls = import_string(v['NAME'])
        options = v.get('OPTIONS', {})
        validators.append(cls(**options))
    return validators
