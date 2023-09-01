from .converter import BrotherLabelConverter
from .devices import BrotherDeviceManager

class BrotherLabel(object):
    def __init__(self, device, strict=False):
        self.strict = strict

        self.converter = BrotherLabelConverter()
        self.devices = BrotherDeviceManager()

        if isinstance(device, str):
            self.device = self.devices[device]
        else:
            self.device = device

    def convert(self, type, images,  **kwargs):
        return self.converter.convert(self.device, type, images, **kwargs)
