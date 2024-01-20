from django.contrib import admin
from .models import Birthday, BirthdayNote, Memo, Category
# Register your models here.


class BirthdayNoteInline(admin.TabularInline):
    model = BirthdayNote


class BirthdayAdmin(admin.ModelAdmin):
    inlines = (BirthdayNoteInline,)
    search_fields = ('person',)
    readonly_fields = ('id',)


class BirthdayNoteAdmin(admin.ModelAdmin):
    search_fields = ('birthday__person',)
    list_display = ('birthday', 'title', 'pub_date')
    readonly_fields = ('pub_date', 'id')


class MemoAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'id', 'last_modified', 'slug')
    list_display = ('pub_date', 'last_modified', 'title', 'status', 'category')


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Birthday, BirthdayAdmin)
admin.site.register(BirthdayNote, BirthdayNoteAdmin)
admin.site.register(Memo, MemoAdmin)
admin.site.register(Category, CategoryAdmin)
