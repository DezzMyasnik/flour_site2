from django.db import models
#from django.db.models.fields.duration import DurationField
from datetime import datetime, timedelta
from .compress import compress
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField()
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name




#Кухня--------------------------------------------
class Kitchen(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухня'

    def __str__(self):
        return self.name


class KitchenGallary(models.Model):
    image = models.ImageField(upload_to='kitchen', blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='images', null=True)

    def __str__(self):
        return "%s %s" % (self.kitchen, self.image)

    def save(self, *args, **kwargs):
        # call the compress function
        if self.image:
            new_image = compress(self.image)
            # set self.image to new_image
            self.image = new_image
        # save
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "images"
#------------------------------------------------


#Блюда-------------------------------------------
class Dishes(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    #kitchen = models.ForeignKey(Kitchen, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        #ordering = ("name",)
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name

class DishesGallary(models.Model):
    image = models.ImageField(upload_to='dishes', blank=True)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, related_name='images', null=True)

    def __str__(self):
        return "%s %s" % (self.dish, self.image)

    def save(self, *args, **kwargs):
        # call the compress function
        if self.image:
            new_image = compress(self.image)
            # set self.image to new_image
            self.image = new_image
        # save
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "images"
#-------------------------------------------------


class DishFormat(models.Model):
    pos = models.IntegerField(default=1, verbose_name='Порядок приготовления')
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE,  verbose_name='Блюдо')

    class Meta:
        ordering =('pos',)

    def __str__(self):
        return '{}: {}'.format(self.pos, self.dish.name)

class Product(models.Model):

    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, verbose_name='Категория')
    kitchen = models.ForeignKey(Kitchen, related_name='kitchen', on_delete=models.CASCADE, verbose_name='Вид кухни')
    dishes = models.ManyToManyField(DishFormat, related_name='dishes',
                                    verbose_name='Состав блюд')  # , on_delete=models.CASCADE)
    # dict_dishes = models.ManyToManyField(FormattedDishes,related_name='dict_dishes')

    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='product', blank=True)
    description = models.TextField(blank=True)
    dateofevent = models.DateTimeField(null=True, editable=True, blank=True, verbose_name='Дата проведения')
    duration = models.DurationField(default=timedelta(hours=1), verbose_name='Длительность')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена билета')
    quantity = models.PositiveIntegerField(default=10, verbose_name='Осталось мест')
    stock = models.PositiveIntegerField(verbose_name='Всего мест')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Мастер-классы"
        ordering = ('dateofevent',)
        index_together = (('id', 'slug'),)
        # verbose_name = 'Мероприятие'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # call the compress function
        if self.image:
            new_image = compress(self.image)
            # set self.image to new_image
            self.image = new_image
        # save
        super().save(*args, **kwargs)

