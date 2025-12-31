from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Commande)
admin.site.register(User)
admin.site.register(ItemCommande)
admin.site.register(ItemVendor)