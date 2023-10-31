import pathlib
import glob
import json


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)

file_info = dict()
files = [file for file in glob.glob("*.yaml")]
for file_name in files:
    with open(file_name, 'rb') as fp:
        c_generator = _count_generator(fp.raw.read)
        # count each \n
        count = sum(buffer.count(b'\n') for buffer in c_generator)
        file_info[file_name] = count
        # print('The filename:{} && Total lines:{}'.format(file_name, count))

#  Serializing json
json_object = json.dumps(file_info, indent=4)

with open("../workflow_line_info.json", "w") as outfile:
    outfile.write(json_object)
