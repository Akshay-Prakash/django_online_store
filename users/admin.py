from curses.ascii import US
from re import U
from django.contrib import admin

from users.models import User, Address

admin.site.register(User)
admin.site.register(Address)
