from django.contrib import admin

from .models import Load, Post, ScienceDegree, ScienceTitle, Field, UploadFile, PlanFile, Request


# Register your models here.

# field, plan files, upload files
class FieldAdmin(admin.ModelAdmin):
    model = Field
    list_display = (
        'owner',
        'type_of_load',
        'load_type',
        'name_in_load',
        'name_in_plan',
        'column_in_load',
        'column_in_plan',
    )

    # list_editable = (
    #     'adopted_fields',
    # )
    # list_filter = (
    #     'adopted_fields',
    # )
    # list_select_related = ('adopted_fields', )
    # search_fields = (
    #     'first_name',
    #     'last_name',
    # )
    # # actions = (
    # #     make_black_listed,
    # # )


class PlanFileAdmin(admin.ModelAdmin):
    model = PlanFile
    list_display = (
        'file',
        'owner',
    )


class UploadFileAdmin(admin.ModelAdmin):
    model = UploadFile
    list_display = (
        'file',
        'owner',
    )


class RequestAdmin(admin.ModelAdmin):
    model = Request
    list_display = (
        'create_date',
        'answer_date',
        'sender',
        'receiver',
        'result'
    )


admin.site.register(Load)
admin.site.register(Post)
admin.site.register(ScienceDegree)
admin.site.register(ScienceTitle)
admin.site.register(Field, FieldAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(PlanFile, PlanFileAdmin)
admin.site.register(Request, RequestAdmin)
