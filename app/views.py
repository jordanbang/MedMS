import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from models import Availability, PatientRequests
from sms_service import SmsService

from django.contrib.auth.models import User
from .models import Doctor

sms_sender = SmsService()


# Create your views here.
def index(request):
    context = {}

    return render(request, "app/index.html", context)


def open_requests(request):
    context = dict(calls=PatientRequests.objects.filter(open=True))

    return render(request, "app/calls.html", context)


def open_requests_respond(request):
    if request.method == 'POST':
        number = request.POST.get("patient")
        failed_messages = respond_to_patient_request(number)

    return redirect("/app/open_requests/")


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

        doctor_ack = number_extractor(body)

        if doctor_ack:
            resp = sms_sender.reply_to_doctor()
            failed_messages = respond_to_patient_request(doctor_ack)

        else:
            resp = sms_sender.reply_to_patient()
            location = location_extractor(body)
            PatientRequests(patient=from_number, location=location, open=True).save()
            sos = "Dear MedMS volunteers. A patient with the following number: {} is requesting assistance. " \
                  "Patient's message: {}".format(from_number, body)
            failed_messages = sms_sender.send_new_message(sos, get_available_doctors())

        return HttpResponse(str(resp))

    else:
        return HttpResponse(str(get_available_doctors()))


@require_http_methods(["GET"])
def signup(request):
    context = {}
    return render(request, "app/signup.html", context)


def signup_submit(request):
    if request.method == 'POST':
        print(str(request.POST))
        data = request.POST

        user = User.objects.create_user(username=data["email"], email=data["email"],
                                        password=data["password"], first_name=data["first"],
                                        last_name=data["last"])
        user.save()
        doctor = Doctor(user=user, phone=data["phone"], location=data["location"])
        doctor.save()

        print("it worked !")
        return HttpResponse("It worked!")
    else:
        print("it failed !")
        return HttpResponse("It failed")


@require_http_methods(["GET"])
def signup(request):
    context = {}
    return render(request, "app/signup.html", context)


def signup_submit(request):
    if request.method == 'POST':
        data = request.POST

        user = User.objects.create_user(username=data["email"], email=data["email"],
                                        password=data["password"], first_name=data["first"],
                                        last_name=data["last"])
        user.save()
        doctor = Doctor(user=user, phone=data["phone"], location=data["location"])
        doctor.save()

        #TODO: redirect this to Doctor page
        print("it worked !")
        return HttpResponse("It worked!")
    else:
        print("it failed !")
        return HttpResponse("It failed")


def medms_login(request):
    context = {}
    return render(request, 'app/login.html', context)


def login_submit(request):
    if request.method == 'POST':
        data = request.POST

        username = data["email"]
        password = data["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print("active user authenticated")
                login(request, user)
                return redirect('/app/account/')

        return HttpResponseNotFound("Login failed, try again")


@login_required(login_url='/app/login/')
def account(request):
    context = {}
    return render(request, 'app/loggedin.html', context)


#######################################################################################################################
# The following are helper funcions
def location_extractor(msg):
    words = msg.lower().split(' ')
    try:
        loc = words.index('location')
        location = words[loc + 1]
    except:
        location = 'Unspecified'
    return location.upper()


def respond_to_patient_request(number):
    patients = PatientRequests.objects.filter(patient=number, open=True)
    for req in patients:
        req.open = False
        req.save()

    patient_reply = 'Dear MedMS patient, a doctor has acknowledged your request for assistance. ' \
                    'You should expect to hear from them shortly.'
    failed_messages = sms_sender.send_new_message(patient_reply, [number])
    return failed_messages


def number_extractor(msg):
    words = msg.lower().split(' ')
    if words[0][1:].isdigit():
        return words[0]
    else:
        return None


def get_available_doctors():
    now = datetime.datetime.now()
    today = now.isoweekday()
    available_doctors = Availability.objects.filter(day=today, start__lte=now, end__gte=now)
    doctors = [x.doctor.phone for x in available_doctors]
    return doctors
