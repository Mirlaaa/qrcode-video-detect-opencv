import uuid, qrcode
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    attendance_indentifier = models.UUIDField(unique=True, default=uuid.uuid4)
    check_in_qr_code = models.ImageField(upload_to="checkin/qrcode/", blank=True)
    is_attendance_confirmed = models.BooleanField(default=False)


@receiver(pre_save, sender=Subscription)
def generate_check_in_qr_code(sender, instance, raw, **kwargs):
    if not instance.check_in_qr_code:
        identifier = instance.attendance_indentifier
        qr_image = qrcode.make(identifier)
        
        img_io = BytesIO()
        qr_image.save(img_io, format="PNG")

        qrcode_path = "{}.png".format(identifier)
        instance.check_in_qr_code = ContentFile(img_io.getvalue())
        instance.check_in_qr_code.name=qrcode_path

