from django.contrib import admin
from .models import Birthday, BirthdayNote, Memo, Category
# Register your models here.


class BirthdayNoteInline(admin.TabularInline):
    """
    Inline display class for the BirthdayNote model.
    """
    model = BirthdayNote


class BirthdayAdmin(admin.ModelAdmin):
    """
    Admin display class for the Birthday model.
    """
    inlines = (BirthdayNoteInline,)
    search_fields = ('person',)
    readonly_fields = ('id',)


class BirthdayNoteAdmin(admin.ModelAdmin):
    """
    Admin display class for the BirthdayNote model.
    """
    search_fields = ('birthday__person',)
    list_display = ('birthday', 'title', 'pub_date')
    readonly_fields = ('pub_date', 'id')


class MemoAdmin(admin.ModelAdmin):
    """
    Admin display for the Memo model.
    """
    readonly_fields = ('pub_date', 'id', 'last_modified', 'slug')
    list_display = ('pub_date', 'last_modified', 'title')


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin display for the Category model.
    """
    readonly_fields = ('id',)


admin.site.register(Birthday, BirthdayAdmin)
admin.site.register(BirthdayNote, BirthdayNoteAdmin)
admin.site.register(Memo, MemoAdmin)
admin.site.register(Category, CategoryAdmin)
