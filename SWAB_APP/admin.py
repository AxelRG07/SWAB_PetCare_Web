from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('tipo', )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('tipo', )}),

    )
admin.site.register(Refugio)
admin.site.register(Mascota)
admin.site.register(Adopcion)
