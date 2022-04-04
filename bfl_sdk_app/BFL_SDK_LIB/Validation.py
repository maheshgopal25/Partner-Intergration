import re
from .Validity import Validity


class Validation(object):
    isValid = False

    # def isNumeric(self, param):
    #     return True if re.search("^[0-9]+$", param) else False
    #
    # def isAlphaNum(self, param):
    #     return True if re.search("^[a-zA-Z0-9.:_ ]*$", param) else False
    #
    # def isChar(self, param):
    #     return True if re.search("^[a-zA-Z]+$", param) else False

    def CheckDataType(self, param, my_re):
        #print(param, my_re)
        #print(True if re.search(my_re, param) else False)
        return True if re.search(my_re, param) else False


    def isMandatory(self, fieldvalue):
        if not fieldvalue.specs.IsMandatory == "Yes":
            return True
        else:
            return bool(int(len(fieldvalue.value) != 0))

    def ValidateField(self, fieldvalue, bfl_config_data):
        cvalidity = Validity()
        isMandatory = self.isMandatory(fieldvalue)
        isValidateDatatype = self.validateDataType(fieldvalue, bfl_config_data)
        isValidateMinLen = self.validateMinLen(fieldvalue)
        isValidateMaxLen = self.validateMaxLen(fieldvalue)
        if isMandatory and isValidateDatatype and isValidateMinLen and isValidateMaxLen == True:
            cvalidity.isValid = True
            cvalidity.JsonTag = fieldvalue.specs.JsonTag
        else:
            if isValidateDatatype != True:
                cvalidity.isValid = False
                cvalidity.JsonTag = fieldvalue.specs.JsonTag
                cvalidity.Message = "Please check the DataType"
            if isValidateMaxLen != True or isValidateMinLen != True:
                cvalidity.isValid = False
                cvalidity.JsonTag = fieldvalue.specs.JsonTag
                cvalidity.Message = "Please check the Min or Max length of in the input value"
        return cvalidity

    def validateDataType(self, fieldvalue, bfl_config_data):
        if fieldvalue.specs.IsMandatory == "Yes":
            if fieldvalue.specs.DataType == "N":
                return self.CheckDataType(fieldvalue.value, bfl_config_data["Numeric"])
            elif fieldvalue.specs.DataType == "AN":
                return self.CheckDataType(fieldvalue.value, bfl_config_data["AlphaNumeric"])
            elif fieldvalue.specs.DataType == "C":
                return self.CheckDataType(fieldvalue.value, bfl_config_data["Char"])
            elif fieldvalue.specs.DataType == "D":
                return self.CheckDataType(fieldvalue.value, bfl_config_data["Decimal"])
            return False
        return True

    def validateMinLen(self, fieldvalue):
        if fieldvalue.specs.IsMandatory == "Yes":
            return bool(int(len(fieldvalue.value) >= int(fieldvalue.specs.Min_len)))
        return True

    def validateMaxLen(self, fieldvalue):
        if fieldvalue.specs.IsMandatory == "Yes":
            return bool(int(len(fieldvalue.value) <= int(fieldvalue.specs.Max_len)))
        return True


valid = Validation()
