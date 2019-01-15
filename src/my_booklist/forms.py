from django.forms import ModelForm, TextInput
from .models import Book


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ('isbn', 'title', 'subtitle', 'author1', 'author2', 'author3', 'author4', 'category')

        labels = {
            'isbn': 'ISBN',
            'title': '書名',
            'subtitle': '副題',
            'author1': '著者',
            'category': '分類',
        }

        widgets = {
            'title': TextInput(attrs={'size': 42}),
            'subtitle': TextInput(attrs={'size': 42}),
            'author1': TextInput(attrs={'size': 20}),
            'author2': TextInput(attrs={'size': 20}),
            'author3': TextInput(attrs={'size': 20}),
            'author4': TextInput(attrs={'size': 20}),
        }
