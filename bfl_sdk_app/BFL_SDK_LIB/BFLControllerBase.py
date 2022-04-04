from .Common import Common
from .Validation import Validation
from .FieldValue import FieldValue
from .Validity import Validity
from .AESService import AESCipher


class BaseControllerBase(object):
    common = Common()
    return_message = None
    validity_list = []

    def validate_apiname(self, apiName):
        if apiName == '':
            self.return_message = "Api name should not be blank"
            return self.return_message

    def validate_common_message(self):
        if not self.common.returnMessage == "Success":
            self.return_message = "Request.json file not found or there is no data"
            return self.return_message

    def validate_bfl_data(self):
        if self.bfl_config_data == '':
            self.return_message = "BFLAppConfig.json file not found or there is no data"
            return self.return_message
        if self.bfl_config_data['BaseUrl'] == '':
            self.return_message = "BaseUrl has not provided"
            return self.return_message
        if self.bfl_config_data['IV'] == '':
            self.return_message = "IV value has not provided"
            return self.return_message
        if self.bfl_config_data['SupplierIDPOD'] == '':
            self.return_message = "POD SupplierID has not provided"
            return self.return_message
        if self.bfl_config_data['Decimal'] == '':
            self.return_message = "Decimal has not provided"
            return self.return_message
        if self.bfl_config_data['AlphaNumeric'] == '':
            self.return_message = "AlphaNumeric has not provided"
            return self.return_message
        if self.bfl_config_data['Numeric'] == '':
            self.return_message = "Numeric has not provided"
            return self.return_message
        if self.bfl_config_data['Char'] == '':
            self.return_message = "Char has not provided"
            return self.return_message

    def __init__(self, data):
        self.bfl_config_data = self.common.load_bfl_config_data()
        self.common.currentApiName = data['ApiName']
        self.common.load_specs(self.common.currentApiName)
        for key, value in data.items():
            if key == self.bfl_config_data['SupplierIDLabel']:
                self.common.supplierId = value
        self.common.currentApiUrl = self.bfl_config_data['BaseUrl']

    def set_value(self, listPartnerInput):
        try:
            if not listPartnerInput:
                self.return_message = "Input values not found"
                return self.return_message
            for key, value in listPartnerInput.items():
                self.common.setValueHelper(key, value)
        except Exception as e:
            print(e)

    def send_request_async(self):
        validation = Validation()
        set_valid_data = []
        responseDict = []
        try:
            data = self.common.load_specs(self.common.currentApiName)
            mapped_data = {self.common.setData.JsonTag[i]: self.common.setData.value[i] for i in
                           range(len(self.common.setData.value))}

            for i in data:
                if not i['JsonTag'] in self.common.setData.JsonTag:
                    self.return_message = i['JsonTag'] + " Input data not found in"
                    return self.return_message

            for key, value in mapped_data.items():
                for i in data:
                    if key == i['JsonTag'] and i['IsMandatory'] == "Yes" and value == '':
                        self.return_message = "is mandatory but data not provide  " + i['JsonTag']
                        return self.return_message
            for i in data:
                for key, value in mapped_data.items():
                    cField_value = FieldValue()
                    cField_value.specs.Id = i['Id']
                    cField_value.specs.JsonTag = i['JsonTag']
                    cField_value.specs.Min_len = i['Min_len']
                    cField_value.specs.Max_len = i['Max_len']
                    cField_value.specs.IsMandatory = i['IsMandatory']
                    cField_value.specs.DataType = i['DataType']
                    cField_value.value = value
                    isFiled_value = validation.ValidateField(cField_value, self.bfl_config_data)
                    cvalidity = Validity()
                    cvalidity.JsonTag = key
                    cvalidity.isValid = isFiled_value
                    # print(cvalidity.isValid.JsonTag, cvalidity.JsonTag, isFiled_value.isValid)
                    #print(cvalidity.isValid.JsonTag, cvalidity.JsonTag, isFiled_value.JsonTag)
                    self.validity_list.append(cvalidity)
                    if cvalidity.isValid.JsonTag == cvalidity.JsonTag == isFiled_value.JsonTag:
                        responseDictval = {"JsonTag": isFiled_value.JsonTag, "isValid": isFiled_value.isValid, "Message": isFiled_value.Message}
                        responseDict.append(responseDictval)
                        set_valid_data.append(isFiled_value.isValid)
            isValid = set_valid_data.count(False)
            if isValid == 0:
                obj = AESCipher(self.bfl_config_data['IV'], self.bfl_config_data['KEY'])
                # print("request body", self.common.get_request_body())
                encryptData = obj.encrypt(self.common.get_request_body())
                self.common.sealValue = obj.hash((encryptData + self.bfl_config_data['KEY'].encode('ascii')))
                apiResponse = self.common.api_request('"' + str(encryptData) + '"')
                # print(apiResponse)
                message = apiResponse.replace('"', "").replace("\\", "")
                dycrypt_new = message[:message.rfind("|")]
                response = obj.decrypt(dycrypt_new)
                return response
            else:
                self.return_message = "Please check input data into respective fields"
                return responseDict
        except Exception as e:
            print(e)
