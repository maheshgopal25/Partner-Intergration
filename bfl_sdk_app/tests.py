from bfl_sdk_app.BFL_SDK_LIB.Common import Common
from bfl_sdk_app.BFL_SDK_LIB.BFLControllerBase import BaseControllerBase
from bfl_sdk_app.BFL_SDK_LIB.FieldValue import FieldValue
from bfl_sdk_app.BFL_SDK_LIB.Validation import Validation

import unittest


class BflTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BflTests, self).__init__(*args, **kwargs)
        self.common = Common()
        self.validation = Validation()
        self.field_value = FieldValue()

    def test_empty_api_name(self):
        res = BaseControllerBase.validate_apiname(self, "")
        self.assertEqual(res, 'Api name should not be blank')

    def test_valid_api_name(self):
        res = BaseControllerBase.validate_apiname(self, "Requery")
        self.assertIsNone(res)

    def test_invalid_validate_common_message(self):
        self.common.returnMessage = "Something"
        res = BaseControllerBase.validate_common_message(self)
        self.assertEqual(res, "Request.json file not found or there is no data")

    def test_valid_validate_common_message(self):
        self.common.load_specs('CancelledTransaction')
        res = BaseControllerBase.validate_common_message(self)
        self.assertEqual(self.common.returnMessage, "Success")
        self.assertIsNone(res)

    def test_validate_bfl_data(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = self.common.load_bfl_config_data()
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertIsNone(res)

    def test_bfl_config_data_isEmpty(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = ""
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertEqual(res, "BFLAppConfig.json file not found or there is no data")

    def test_bfl_config_data_baseUrl_isEmpty(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = {'BaseUrl': ''}
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertEqual(res, "BaseUrl has not provided")

    def test_bfl_config_data_iV_isEmpty(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = {'BaseUrl': 'www.google.com', 'IV': ''}
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertEqual(res, "IV value has not provided")

    def test_bfl_config_data_suplierPod_isEmpty(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = {'BaseUrl': 'www.google.com', 'IV': '1234553423434', 'SupplierIDPOD': ''}
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertEqual(res, "POD SupplierID has not provided")

    def test_valid_bfl_config_data_method(self):
        dict = {'ApiName': 'CancelledTransaction'}
        BaseControllerBase(dict)
        data = {'BaseUrl': 'www.google.com', 'IV': '1234553423434', 'SupplierIDPOD': '12'}
        self.bfl_config_data = data
        res = BaseControllerBase.validate_bfl_data(self)
        self.assertIsNone(res)

    def test_set_value(self):
        self.common.load_specs('CancelledTransaction')
        data = {}
        self.return_message = ""
        BaseControllerBase.set_value(self, data)
        self.assertEqual(self.return_message, "Input values not found")

    def test_setValue_helper(self):
        data = {'CARDNUMBER': '2030408899771011', 'ORDERNO': 'ECOMREST141220201420', 'DEALERID': '95',
                'VALIDATIONKEY': 'qasas1212', 'REQUESTID': 'ECOMREST141220201420', 'REQUESTDATE1': '',
                'REQUESTDATE2': '', 'REQUESTTEXT1': '', 'REQUESTTEXT2': '', 'Manufacturer': 'ABSC11', 'ASSETID': '1',
                'LOANAMT': '12000', 'TncACCEPT': 'Y', 'OTPNO': '', 'NAMEONCARD': '', 'IPADDR': '10.10.12.100',
                'Tenure': '10', 'PIN': '123456', 'SALETYPE': '43534534dfgd', 'PRODDESC': 'Apple Iphone 7',
                'SCHEMEID': '175', 'MOBILENO': ''}

        self.common.load_specs('CancelledTransaction')
        self.return_message = ""
        json = ['CARDNUMBER', 'ORDERNO', 'DEALERID', 'VALIDATIONKEY', 'REQUESTID', 'REQUESTDATE1', 'REQUESTDATE2',
                'REQUESTTEXT1', 'REQUESTTEXT2', 'Manufacturer', 'ASSETID', 'LOANAMT', 'TncACCEPT', 'OTPNO',
                'NAMEONCARD', 'IPADDR', 'Tenure', 'PIN', 'SALETYPE', 'PRODDESC', 'SCHEMEID', 'MOBILENO']
        value = ['2030408899771011', 'ECOMREST141220201420', '95', 'qasas1212', 'ECOMREST141220201420', '', '', '', '',
                 'ABSC11', '1', '12000', 'Y', '', '', '10.10.12.100', '10', '123456', '43534534dfgd', 'Apple Iphone 7',
                 '175', '']
        BaseControllerBase.set_value(self, data)
        self.assertEqual(self.common.setData.JsonTag, json)
        self.assertEqual(self.common.setData.value, value)

    def test_isNumeric_true(self):
        self.assertTrue(self.validation.isNumeric('1234'))

    def test_isNumaric_false(self):
        self.assertFalse(self.validation.isNumeric('abcd'))

    def test_isAlphaNum_true(self):
        self.assertTrue(self.validation.isAlphaNum('1234abcd'))

    def test_isAlphaNum_false(self):
        self.assertFalse(self.validation.isAlphaNum('(&*('))

    def test_isChar_true(self):
        self.assertTrue(self.validation.isChar('Y'))

    def test_isChar_false(self):
        self.assertFalse(self.validation.isChar('1'))

    def test_isMandatory_no(self):
        self.field_value.specs.IsMandatory = "No"
        self.assertTrue(self.validation.isMandatory(self.field_value))

    def test_isMandatory_value_true(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = '12345'
        self.assertTrue(self.validation.isMandatory(self.field_value))

    def test_isMandatory_value_false(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = ''
        self.assertFalse(self.validation.isMandatory(self.field_value))

    def test_validateMinLen_true(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = '12345121212121221212'
        self.field_value.specs.Min_len = 10
        self.assertTrue(self.validation.validateMinLen(self.field_value))

    def test_validateMinLen_false(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = '1212212'
        self.field_value.specs.Min_len = 20
        self.assertFalse(self.validation.validateMinLen(self.field_value))

    def test_validateMaxLen_true(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = "123"
        self.field_value.specs.Max_len = 10
        self.assertTrue(self.validation.validateMaxLen(self.field_value))

    def test_validateMaxLen_false(self):
        self.field_value.specs.IsMandatory = "Yes"
        self.field_value.value = "1212121212121"
        self.field_value.specs.Max_len = 2
        self.assertFalse(self.validation.validateMaxLen(self.field_value))
