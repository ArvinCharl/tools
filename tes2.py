import base64


def base64_to_file(input_base64_file, out_ori_file):
    with open(input_base64_file, 'r') as f:
        base64_data = f.read()
        ori_data = base64.b64decode(base64_data)
        with open(out_ori_file, 'wb') as f1:
            f1.write(ori_data)


def file_to_base64(infile, outfile):
    with open(infile, 'rb') as fileObj:
        file_data = fileObj.read()
        base64_data = base64.b64encode(file_data)
        with open(outfile, 'wb') as f:
            f.write(base64_data)
        return base64_data


with open('no_mask.mp4', 'rb') as fileObj:
    file_data = fileObj.read()
    base64_data = base64.b64encode(file_data)
    print(base64_data.decode())
#     # with open('no_mask.txt', 'wb') as f:
#     #     f.write(base64_data)
#     f = open('no_mask.txt', '')

with open('no_mask.txt', 'rb') as f:
    base64_data = f.read()
with open('out_mask.mp4', 'wb') as f1:
    f1.write(base64_data)

# if __name__ == '__main__':
#     file_to_base64(r'no_mask.mp4', 'no_mask.txt')
#     base64_to_file('no_mask.txt', 'out_no_mask.mp4')
