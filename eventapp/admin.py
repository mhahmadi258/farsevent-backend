from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, Ticket, EventCategory, EventType , Register

DEFAULT_IMAGE_WIDTH = 100


class TicketStackedInline(admin.StackedInline):
    model = Ticket
    show_change_link = True
    fields = [
        'title',
        ('capacity', 'price'),
        'description',
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'city', 'start_time',
                    'event_category', 'event_type')
    list_filter = ('city', 'event_category', 'event_type',)
    search_fields = ('title', 'owner',)
    readonly_fields = ('image_preview',)
    inlines = (TicketStackedInline,)

    fields = [
        ('title', 'owner'),
        ('event_category', 'event_type'),
        ('start_time', 'end_time'),
        'image_preview',
        'image',
        'description',
        'city',
        'address',
        'tags',
    ]

    def image_preview(self, obj):
        url = obj.image.url
        image_tag = f'<img src="{url}" style="width : {DEFAULT_IMAGE_WIDTH}px"/>'
        return mark_safe(image_tag)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('image_preview',)
    fields = [
        'name',
        'image_preview',
        'image',
    ]

    def image_preview(self, obj):
        url = obj.image.url
        image_tag = f'<img src="{url}" style="width : {DEFAULT_IMAGE_WIDTH}px"/>'
        return mark_safe(image_tag)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = [
        'name',
    ]


class RegisterTabularInline(admin.TabularInline): 
    model = Register
    readonly_fields = ('registration_id','register_time')
    fields = [
        'user',
        'registration_id',
        'register_time',
        'condition',
    ]

    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title','event','capacity','price')
    search_fields = ('title','event',)
    fields = [
        ('title','event'),
        ('capacity','price',),
        'description',
    ]
    inlines = (RegisterTabularInline,)
