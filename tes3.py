#!/user/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time
import traceback

"""
rtsp://61.151.156.6:8554/cam/realmonitor?vcuid=fMcmuLZbB1CRSOMNR1645L&subtype=0&urlType=agentPull&manufacturer=HIKVISION&protocoltype=HIKVISION&streamType=0&token=1625534463_89950bac450931f96b81872617d4fd5fb7afc103&mapNet=ExtNet
"""
"""
python tes3.py --accessToken 'accessToken' --token 'testoken' --algorithmInstanceId '00001' --videoURL "http://001.com" "http://002.com" "http://003.com" --cameraId "PJ003" "PJ004" "PJ005" --postDataURL "https://tes111.com"
"""

while True:
    try:
        parser = argparse.ArgumentParser(description='启停接口')
        parser.add_argument('--accessToken', required=True)
        parser.add_argument('--token', required=True)
        parser.add_argument('--algorithmInstanceId', required=True)
        parser.add_argument('--videoURL', nargs='+', required=True)
        parser.add_argument('--cameraId', nargs='+', required=True)
        parser.add_argument('--postDataURL', required=True)
        parser.add_argument('--algorithmParas', nargs='+')
        parser.add_argument('--extensionData', nargs='+')

        args = parser.parse_args()
        print(f'accessToken: {args.accessToken}')
        print(f'token: {args.token}')
        print(f'algorithmInstanceId: {args.algorithmInstanceId}')
        print(f'videoURL: {args.videoURL}')
        print(f'cameraId: {args.cameraId}')
        print(f'postDataURL: {args.postDataURL}')
        print(f'algorithmParas: {args.algorithmParas}')
        print(f'extensionData: {args.extensionData}')
        print('-' * 200, '\n')

        time.sleep(10)
    except:
        traceback.print_exc()

