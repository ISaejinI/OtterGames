from django.contrib import admin
from loginUser.models import customUser

@admin.register(customUser)
class userAdmin(admin.ModelAdmin):
    list_display=('username', 'first_name', 'recompense')