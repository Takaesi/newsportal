from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(total=models.Sum('rating'))['total'] or 0
        post_rating *= 3
        comment_rating = self.user.comment_set.aggregate(total=models.Sum('rating'))['total'] or 0
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('rating'))['total'] or 0
        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()

class Category(models.Model):
    category = models.TextField(unique=True)

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NE'
    POST_TYPES = [
        (ARTICLE, 'статья'),
        (NEWS, 'новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    date_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=45)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    