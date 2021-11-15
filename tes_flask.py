#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    ret = request.get_data()
    dict1 = json.loads(ret)
    print(dict1)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
