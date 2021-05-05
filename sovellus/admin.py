from django.contrib import admin

# Register your models here.

from .models import Post
from .models import Note

admin.site.register(Post)
admin.site.register(Note)
