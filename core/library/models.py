import pendulum
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=300)
    publishedDate = models.DateField()
    authors = models.ManyToManyField('Author')
    categories = models.ManyToManyField('Category', blank=True)
    average_rating = models.IntegerField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    @classmethod
    def create(cls, **kwargs):
        volumeInfo = kwargs['volumeInfo']
        book = cls.objects.create(
            title=volumeInfo['title'],
            publishedDate=pendulum.parse(volumeInfo['publishedDate']).date()
        )

        for authorBook in volumeInfo['authors']:
            author, created = Author.objects.get_or_create(full_name=authorBook)
            book.authors.add(author)
        if 'averageRating' in volumeInfo.keys():
            book.average_rating = volumeInfo['averageRating']
        elif 'categories' in volumeInfo.keys():
            for category in volumeInfo['categories']:
                category, created = Category.objects.get_or_create(title=category)
                book.categories.add(category)
        elif 'imageLinks' in volumeInfo.keys():
            book.thumbnail = volumeInfo['imageLinks']['thumbnail']
        elif 'ratingsCount' in volumeInfo.keys():
            book.ratings_count = volumeInfo['ratingsCount']

        return book

    @classmethod
    def update_or_create(cls, **kwargs):
        volumeInfo = kwargs['volumeInfo']
        updated_values = {}
        if 'averageRating' in volumeInfo.keys():
            updated_values['average_rating'] = volumeInfo['averageRating']
        elif 'imageLinks' in volumeInfo.keys():
            updated_values['thumbnail'] = volumeInfo['imageLinks']['thumbnail']
        elif 'ratingsCount' in volumeInfo.keys():
            updated_values['ratings_count'] = volumeInfo['ratingsCount']

        book, created = cls.objects.update_or_create(
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

        return book


class Author(models.Model):
    full_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.full_name}'


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.title}'


