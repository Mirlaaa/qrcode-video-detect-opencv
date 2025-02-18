import logging, json

from django.http import JsonResponse
from django.shortcuts import render
from .models import Subscription
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def confirm_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            identifier_value = data.get("identifier","")
            subcription_instance = Subscription.objects.get(attendance_indentifier=identifier_value)
            subcription_instance.is_attendance_confirmed=True
            subcription_instance.save()

            user = subcription_instance.user
            return JsonResponse({"message":f"Subscription confirmed for user {user}", "status":200})
        except Exception as exception:
            print(exception)
            logging.exception("An exception was raised during the checkin for identified %s| Exception: %s, Message: %s", 
                            identifier_value, type(exception).__name__, str(exception))
            return JsonResponse({"message":"An error ocurred", 
                                "exceptions": {"type": type(exception).__name__, "message":str(exception)},
                                "status":500})
        
    return JsonResponse()