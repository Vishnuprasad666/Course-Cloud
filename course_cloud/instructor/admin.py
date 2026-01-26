from django.contrib import admin
from instructor.models import User,Category,Course,Module,Lesson
# Register your models here.

admin.site.register(User)
admin.site.register(Category)

class CourseModel(admin.ModelAdmin):
    exclude=("owner",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner=request.user
        return super().save_model(request, obj, form, change)


class LessonInline(admin.TabularInline):
    model=Lesson
    extra=1

class ModuleModel(admin.ModelAdmin):
    inlines=[LessonInline]


admin.site.register(Course,CourseModel)
admin.site.register(Module,ModuleModel)
admin.site.register(Lesson)


