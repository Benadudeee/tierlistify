from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import TierListEntry, TierListPost, Profile, EntryRating, PostTag
from django.contrib.auth.models import User

# Register your models here.

# Registering the Profile User model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

# Registering the TierList Entry/ Post model
class PostTagInline(admin.StackedInline):
    model = TierListPost.tags.through
    extra = 2

class EntryRatingInline(admin.StackedInline):
    model = EntryRating
    extra = 2

class TierListEntries(admin.StackedInline):
    model = TierListEntry
    extra = 4

class TierListPostAdmin(admin.ModelAdmin):
    list_display = ["author", "name"]
    search_fields = ["name", "author"]
    list_filter = ["name"]

    fieldsets = [
        ("Post Info", {"fields": ["name", "author", "description"]})
    ]

    inlines = [TierListEntries, PostTagInline]

class TierListEntryAdmin(admin.ModelAdmin):
    list_display = ["post", "name"]
    list_filter = ["name"]

    fieldsets = [
        ("Entry Info", {"fields": ["name", "post"]})
    ]

    inlines = [EntryRatingInline]



admin.site.unregister(User)

admin.site.register(TierListEntry, TierListEntryAdmin)
admin.site.register(EntryRating)
admin.site.register(User, UserAdmin)
admin.site.register(TierListPost, TierListPostAdmin)
admin.site.register(PostTag)