from django.contrib import admin
from .models import Subscription

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "attendance_indentifier",
        "is_attendance_confirmed",
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Subscription, SubscriptionAdmin)