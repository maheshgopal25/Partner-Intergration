from bfl_sdk_app.BFL_SDK_LIB.BFLControllerBase import BaseControllerBase


class Programs(object):
    def __init__(self):
        self.data = {
            'CARDNUMBER': '2030408899771011',
            'ORDERNO': 'ORD1001',
            'DEALERID': '95',
            'VALIDATIONKEY': '4631096782208794',
            'REQUESTID': 'ecom_1056071',
            'REQUESTDATE1': '',
			'REQUESTDATE2': '',
            'REQUESTTEXT1': '1232.30',
            'REQUESTTEXT2': '12',
            'Manufacturer': 'ABSC11',
            'ASSETID': '1',
            'LOANAMT': '34354.00',
            'TncACCEPT': 'Y',
            'OTPNO': '',
            'NAMEONCARD': '',
            'IPADDR': '10.10.12.100',
            'Tenure': '12',
            'PIN': '123456',
            'SALETYPE': '43534534dfgd',
            'PRODDESC': 'Apple Iphone 7',
            'SCHEMEID': '175',
            'MOBILENO': '',
			'ApiName': 'InitiateOTP'
        }

cls_obj = Programs()
base_obj = BaseControllerBase(cls_obj.data)
check_api_name = base_obj.validate_apiname(cls_obj.data['ApiName'])
if check_api_name:
    print(str(check_api_name))
cls_obj.data.pop('ApiName')
check_common_message = base_obj.validate_common_message()
if check_common_message:
    print(str(check_common_message))
check_bfl_data = base_obj.validate_bfl_data()
if check_bfl_data:
    print(str(check_common_message))
set_val = base_obj.set_value(cls_obj.data)
if set_val:
    print(str(set_val))
response = base_obj.send_request_async()
print(response)
