from django.contrib import admin
from app.models import UserProfile, CreditLine, PaymentPlan

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CreditLine)
admin.site.register(PaymentPlan)