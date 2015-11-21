from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import twilio
from sms_service import SmsService

from django.contrib.auth.models import User
from .models import Doctor

sms_sender = SmsService()
# Create your views here.

def index(request):
    context = {}

    return render(request, "app/index.html", context)


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def receive_sms(request):
    """Respond to a new sms"""

    if request.GET or request.POST:

        if request.GET:
            from_number = request.GET.get('From')
            body = request.GET.get('Body')

        elif request.POST:
            from_number = request.POST.get('From')
            body = request.POST.get('Body')

        resp = twilio.twiml.Response()
        resp.message('Thank you for reaching out to MedMS we will try to connect you to a doctor as soon as possible.')
        sos = "Dear MedMS volunteers. A patient with the following number: {} is requesting assistance. " \
              "Patient's message: {}".format(from_number, body)
        failed_messages = sms_sender.send_new_message(sos, get_available_doctors())

        return HttpResponse('ok good')

    else:
        return HttpResponse('Ok well whatever.')


def get_available_doctors():
    return ['4169488810']


@require_http_methods(["POST"])
def signup(request):
    data = request.POST.get("data")

    user = User(first_name=data["first_name"], last_name=data["last_name"], email=data["email"],
                username=data["first_name"]+data["last_name"])
    user.save()
    doctor = Doctor(user=user, phone=data["phone"], location=data["location"])
    doctor.save()

    return HttpResponse(
            # json.dumps(response_data),
            content_type="application/json"
    )

