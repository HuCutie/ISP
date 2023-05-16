import os
import os.path as op

import cv2
import numpy as np

from pipeline import Pipeline
from utils.yacs import Config

import rawpy


OUTPUT_DIR = './output'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def demo_test_raw():
    cfg = Config('configs/test.yaml')
    pipeline = Pipeline(cfg)

    raw_path = cfg.input.file
    bayer = np.fromfile(raw_path, dtype='uint16', sep='')
    bayer = bayer.reshape((cfg.hardware.raw_height, cfg.hardware.raw_width))

    data, _ = pipeline.execute(bayer)

    output_path = op.join(OUTPUT_DIR, 'test.png')
    output = cv2.cvtColor(data['output'], cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, output)

def demo_intermediate_results():
    cfg = Config('configs/test.yaml')

    pipeline = Pipeline(cfg)
    raw = rawpy.imread(cfg.input.file)
    raw_data = raw.raw_image
    bayer = np.asarray(raw_data)

    # print(raw_data_np.shape)
    # print(raw_data_np.dtype)

    raw_path = cfg.input.file
    # bayer = np.fromfile(raw_path, dtype='uint16', sep='')
    bayer = bayer.reshape((cfg.hardware.raw_height, cfg.hardware.raw_width))

    _, intermediates = pipeline.execute(bayer, save_intermediates=True)
    for module_name, result in intermediates.items():
        output = pipeline.get_output(result)
        output_path = op.join(OUTPUT_DIR, '{}.png'.format(module_name))
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, output)

if __name__ == '__main__':
    print('Processing test raw...')
    # demo_test_raw()
    demo_intermediate_results()