import requests
import json
from BFL_SDK_Proj.settings import BASE_DIR
from .SpecsMaster import specsmaster
from .Specs import Specs
from .PartnerInput import PartnerInput
from urllib3.exceptions import InsecureRequestWarning


class Common(object):
    setData = PartnerInput()
    specs = [{Specs.return_fields()}]
    currentApiName = None
    currentApiUrl = None
    supplierId = None
    sealValue = None
    returnMessage = None

    def setValueHelper(self, JsonTag, value):
        self.setData.JsonTag.append(JsonTag)
        self.setData.value.append(value.strip())

    def get_setting_file(self, apiName):
        try:
            if apiName == self.load_bfl_config_data()['ReQueryLabel']:
                filepath = open(str(BASE_DIR) + "/bfl_sdk_app/ConfigFiles/" + apiName + ".json")
                return filepath
            filepath = open(str(BASE_DIR) + "/bfl_sdk_app/ConfigFiles/" + apiName + "Request.json")
            return filepath
        except Exception as e:
            print(e)

    def load_specs(self, ApiName):
        self.returnMessage = ""
        try:
            f = self.get_setting_file(ApiName)
            json_data = json.load(f)
            self.returnMessage = "Success"
        except Exception as e:
            self.returnMessage = e
            return self.returnMessage
        specsmaster.Request = json_data['Request']
        return json_data['Request']

    def load_bfl_config_data(self):
        try:
            f = open(str(BASE_DIR) + "/bfl_sdk_app/ConfigFiles/BFLAppConfig.json")
            return json.load(f)
        except Exception as e:
            print(e)

    def get_request_body(self):
        request_body = {self.setData.JsonTag[i]: self.setData.value[i] for i in range(len(self.setData.value))}
        ff = str(request_body)
        aa = ff.replace(": ", ":").replace(", ", ",").replace("'", '"')
        return aa

    def api_request(self, data):
        try:
            payload = data.replace("b'", "").replace("'", "")
            headers = {
                'Content-Type': 'application/json',
                'SealValue': self.sealValue,
                'SupplierID': self.supplierId,
            }
            # print(self.sealValue)
            # print(self.supplierId)
            if self.currentApiName == self.load_bfl_config_data()['ReQueryLabel']:
                final_url = self.load_bfl_config_data()['EnhanceReQuery']
            else:
                final_url = self.currentApiUrl + "/" + self.currentApiName
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            response = requests.post(url=final_url, headers=headers, data=payload, verify=False)
            return response.json()
        except Exception as e:
            print(e)


common = Common()
