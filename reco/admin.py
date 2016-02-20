from django.contrib import admin
from reco.models import * 

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Answer)
