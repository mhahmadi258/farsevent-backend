from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import City

DEFAULT_IMAGE_WIDTH = 100
DEFAULT_IMAGE_HEIGHT = 100


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone',)
    list_filter = ('is_staff',)
    readonly_fields = ('image_preview', 'last_login', 'date_joined')
    fieldsets = [
        (None, {'fields': ('username', 'email', 'phone', 'password',)}),
        ('personal info', {'fields': ('first_name', ('last_name',
                                                     'image_preview'), 'image', 'birth_date', 'city', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def image_preview(self, obj):
        url = obj.image.url
        image_tag = f'<img src="{url}" style="width : {DEFAULT_IMAGE_WIDTH}px"/>'
        return mark_safe(image_tag)


admin.site.register(City)
