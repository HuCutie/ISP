import numpy as np

from .basic_module import BasicModule

class DGA(BasicModule):
    def __init__(self, cfg):
        super().__init__(cfg)

    def execute(self, data):
        bayer = data['bayer'].astype(np.float32)

        dga_bayer = bayer * self.cfg.dga
        
        dga_bayer = np.clip(dga_bayer, 0, self.cfg.saturation_values.hdr)

        data['bayer'] = dga_bayer.astype(np.uint16)