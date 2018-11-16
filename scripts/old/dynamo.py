import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('coleman_quest')
scan = table.scan()
items = scan['Items']
linear = next((i for i in items if i['id'] == '70d64881-b25f-4ec3-85a8-2507e19b1a6c'))

import code; code.interact(local={**locals(), **globals()})

70d64881-b25f-4ec3-85a8-2507e19b1a6c
96490823-966a-4b11-ab0a-64f1d7def529
1bd1a727-dd6f-46cf-81fa-06166c43061e
bea5a4b9-2263-46a5-8510-d819b7b8f28c
9055dcb2-e1e2-4af2-be4d-9b1aa8c8c4f0
925e8f8d-ad7d-4be4-b19b-f9e31bc58e45
99519b10-8352-48ac-8573-785be0817dd4
3cf56609-b1be-42c4-a07e-bccbc8814423
f229f441-40c9-470b-a330-6fbe5d9d43a2
fe60f4b3-9a59-4ebf-8ab5-84869c833049
065964ec-c160-4436-acd8-86472c7d6843
fe548b5e-51e8-4dc9-a659-0cdbef210ccf
92160447-beb1-4f58-9c1e-1ae3541fd1e8
1c0dbe0c-2293-459d-95e0-744276cc90e3


num_calibration_samples