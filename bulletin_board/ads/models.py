from django.db import models

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser.username}'



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'



class Adt(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Author')
    adtCategory = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    title = models.CharField(max_length=128, verbose_name='Заголовок объявления')
    text = RichTextUploadingField(blank=True, verbose_name='Контент')
    # photo = models.ImageField(upload_to='photo/%Y/%m/%d/',  verbose_name='Фото')
    rating = models.SmallIntegerField(default=0)


#добавим ссылку на текущий объект. Для того, чтобы при создании объекта или переходе
    #к его деталям не прописывать в каждом дженерике succes_url.
    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостю
        return f'/ads/{self.id}'


class Respond(models.Model):
    responseAdt = models.ForeignKey(Adt, on_delete=models.CASCADE, verbose_name='Adt')
    responseUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    #получил отклик принятие или нет
    acceptResponse = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.responseUser}'


class Subscriber(models.Model):
    subscribersUser = models.ForeignKey(User, on_delete=models.CASCADE)
    adtCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subscribersUser} {self.adtCategory}'



class OneTimeCode(models.Model):
    codeUser = models.OneToOneField(User, on_delete=models.CASCADE)
    oneTimeCode = models.CharField(max_length=128)