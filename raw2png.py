import rawpy
from PIL import Image

def convert_raw_to_png(raw_file, output_file):
    # 使用 rawpy 打开 RAW 文件
    raw = rawpy.imread(raw_file)

    # 将 RAW 转换为 RGB 图像
    rgb = raw.postprocess()

    # 创建 PIL 图像对象
    image = Image.fromarray(rgb)

    # 保存为 PNG 图像
    image.save(output_file)

# 示例用法
raw_file = 'xiaomi.dng'  # 输入的 RAW 文件路径
output_file = 'xiaomi.png'  # 输出的 PNG 文件路径

# 将 RAW 转换为 PNG
convert_raw_to_png(raw_file, output_file)
