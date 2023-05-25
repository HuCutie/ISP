import os
import os.path as op

import cv2
import numpy as np

from pipeline import Pipeline
from utils.yacs import Config

import rawpy
from PIL import Image


OUTPUT_DIR = './output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def demo():
    cfg = Config('configs/test.yaml')
    save_intermediates = True

    pipeline = Pipeline(cfg)
    raw_path = cfg.input.file
    try:
        raw = rawpy.imread(raw_path)
        raw_data = raw.raw_image
        # print(raw.color_matrix)
        # print(raw.camera_whitebalance)
        # print(raw.raw_image.shape)
        # print(raw.raw_pattern)
        # bayer_partten = "".join([chr(raw.color_desc[i]) for i in raw.raw_pattern.flatten()])
        # print(bayer_partten)
        bayer = np.asarray(raw_data)
        pass
    except rawpy.LibRawFileUnsupportedError:
        # bayer = np.fromfile(raw_path, dtype='uint16', sep='')
        bayer = np.array(Image.open(raw_path))
        pass
    
    print('Resolution: ', str(cfg.hardware.raw_width) + ' x ' + str(cfg.hardware.raw_height))
    print('Bit: ', str(cfg.hardware.raw_bit_depth))
    print('Bayer: ', str(cfg.hardware.bayer_pattern))
    
    bayer = bayer.reshape((cfg.hardware.raw_height, cfg.hardware.raw_width))
    
    if save_intermediates:
        _, intermediates = pipeline.execute(bayer, save_intermediates=True)
        for module_name, result in intermediates.items():
            output = pipeline.get_output(result)
            output_path = op.join(OUTPUT_DIR, '{}.png'.format(module_name))
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, output)
    else:
        data, _ = pipeline.execute(bayer)
        output_path = op.join(OUTPUT_DIR, 'output.png')
        output = cv2.cvtColor(data['output'], cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, output)

    

if __name__ == '__main__':
    print('Processing test raw...')
    demo()