from django.contrib import admin

from .models import Book, Category, Author

class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "publishedDate"]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
