from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from sms_service import SmsService

sms_sender = SmsService()
# Create your views here.

def index(request):
    return HttpResponse("What up?")

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def receive_sms(request):
    """Respond to a new sms"""

    from_number = request.POST.get('From')
    body = request.POST.get('Body')

    resp = sms_sender.reply_to_message()
    sos = "Dear MedMS volunteers. A patient with the following number: {} is requesting assistance. " \
          "Patient's message: {}".format(from_number, body)
    failed_messages = sms_sender.send_new_message(sos, get_available_doctors())

    return str(resp)


def get_available_doctors():
    return ['4169488810']
