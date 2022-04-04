from django.views.generic import TemplateView
from django.http.response import HttpResponse
from bfl_sdk_app.BFL_SDK_LIB.BFLControllerBase import BaseControllerBase
from django.views import View


class OtpAcceptRequest(TemplateView):
    template_name = 'Otp.html'


class AuthAcceptRequest(TemplateView):
    template_name = 'Auth.html'


class CancelAcceptRequest(TemplateView):
    template_name = 'Cancel.html'


class PodRequestAcceptRequest(TemplateView):
    template_name = 'PodRequest.html'


class EligibilityRequestAcceptRequest(TemplateView):
    template_name = 'Eligibility.html'


class ReQueryRequestAcceptRequest(TemplateView):
    template_name = 'Requery.html'

class EnReQueryRequestAcceptRequest(TemplateView):
    template_name = 'ERequery.html'


class DataReceive(View):
    def post(self, request):
        try:
            data = request.POST.dict()
            base_obj = BaseControllerBase(data)
            check_api_name = base_obj.validate_apiname(data['ApiName'])
            if check_api_name:
                return HttpResponse(str(check_api_name))
            data.pop('ApiName')
            check_common_message = base_obj.validate_common_message()
            if check_common_message:
                return HttpResponse(str(check_common_message))
            check_bfl_data = base_obj.validate_bfl_data()
            if check_bfl_data:
                return HttpResponse(str(check_common_message))
            set_val = base_obj.set_value(data)
            if set_val:
                return HttpResponse(str(set_val))
            response = base_obj.send_request_async()
            return HttpResponse(str(response))
        except Exception as e:
            print(e)
