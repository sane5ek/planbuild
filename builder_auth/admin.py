from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.

# def make_black_listed(model_admin, request, queryset):
#     queryset.update(our_note="Don't deliver pizza to this user.")


# make_black_listed.short_description = 'Makes a black-listed note for a user'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # fieldsets = UserAdmin.fieldsets + (
    #     ('Pizza', {'fields': (
    #         'favourite_pizza',
    #         'our_note',
    #     )}),
    # )


    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'adopted_fields',
    )
    list_editable = (
        'adopted_fields',
    )
    list_filter = (
        'adopted_fields',
    )
    list_select_related = ('adopted_fields', )
    search_fields = (
        'first_name',
        'last_name',
    )
    # actions = (
    #     make_black_listed,
    # )

admin.site.register(CustomUser, CustomUserAdmin)
