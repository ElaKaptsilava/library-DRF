import django_filters
import pendulum
import requests

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .models import Author, Category
from .serializer import BookSerializer, AuthorSerializer, CategorySerializer


class BookFilterSet(django_filters.FilterSet):
    authors = django_filters.ModelMultipleChoiceFilter(field_name='authors__full_name', to_field_name='full_name',
                                                       queryset=Author.objects.all())
    bookId = django_filters.NumberFilter(field_name='id')
    publishedDate = django_filters.DateFilter(field_name='publishedDate')

    class Meta:
        model = models.Book
        fields = ['id', 'authors', 'publishedDate']


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['publishedDate']
    filterset_class = BookFilterSet

    @action(detail=False, url_path='db', methods=['POST', 'GET'])
    def db(self, request, *args, **kwargs):
        books = self.get_queryset()
        link = requests.get('https://www.googleapis.com/books/v1/volumes?q=war')
        with link:
            for item in link.json()['items']:
                volumeInfo = item['volumeInfo']
                updated_values = {}
                if 'averageRating' in volumeInfo.keys():
                    updated_values['average_rating'] = volumeInfo['averageRating']
                elif 'imageLinks' in volumeInfo.keys():
                    updated_values['thumbnail'] = volumeInfo['imageLinks']['thumbnail']
                elif 'ratingsCount' in volumeInfo.keys():
                    updated_values['ratings_count'] = volumeInfo['ratingsCount']
                book, created = books.update_or_create(
                    title=volumeInfo['title'],
                    publishedDate=pendulum.parse(volumeInfo['publishedDate']).date(),
                    defaults=updated_values
                )

                for authorBook in volumeInfo['authors']:
                    author, created = Author.objects.get_or_create(full_name=authorBook)
                    book.authors.add(author)

                if 'categories' in volumeInfo.keys():
                    for category in volumeInfo['categories']:
                        category, created = Category.objects.get_or_create(title=category)
                        book.categories.add(category)

            return Response("updated")

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
