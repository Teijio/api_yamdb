import csv

from django.core.management.base import BaseCommand

from reviews.models import (Title, Category, Genre,
                            GenreTitle, User, Review, Comment)


class Command(BaseCommand):
    with open("static/data/genre.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            genre = Genre(
                pk=row[0],
                name=row[1],
                slug=row[2],
            )
            genre.save()

    with open("static/data/category.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            category = Category(
                pk=row[0],
                name=row[1],
                slug=row[2],
            )
            category.save()

    with open("static/data/titles.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            category, _ = Category.objects.get_or_create(pk=int(row[3]))
            title = Title(
                pk=row[0],
                name=row[1],
                year=row[2],
                category=category,
            )
            title.save()

    with open("static/data/genre_title.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            title, _ = Title.objects.get_or_create(pk=int(row[1]))
            genre, _ = Genre.objects.get_or_create(pk=int(row[2]))
            genre_title = GenreTitle(
                pk=row[0],
                title=title,
                genre=genre,
            )
            genre_title.save()

    with open("static/data/users.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            user = User(
                pk=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
            user.save()

    with open("static/data/review.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            title, _ = Title.objects.get_or_create(pk=int(row[1]))
            author, _ = User.objects.get_or_create(pk=int(row[3]))
            review = Review(
                pk=row[0],
                title=title,
                text=row[2],
                author=author,
                score=row[4],
                pub_date=row[5],
            )
            review.save()

    with open("static/data/comments.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            review, _ = Review.objects.get_or_create(pk=int(row[1]))
            author, _ = User.objects.get_or_create(pk=int(row[3]))
            comment = Comment(
                pk=row[0],
                review=review,
                text=row[2],
                author=author,
                pub_date=row[4],
            )
            review.save()

    def handle(self, *args, **options):
        pass
