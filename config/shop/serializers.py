from rest_framework import serializers

from .models import Product, Dishes, DishesGallary, KitchenGallary, Kitchen,DishFormat,  Category

#Кухня---------------------------------------------
class KitchenGallarySerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenGallary
        fields = ('image',)

class KitchenFromProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('kitchen',)


class KitchenSerializer(serializers.ModelSerializer):

    images = KitchenGallarySerializer(many=True)
    class Meta:
        model = Kitchen
        #fields = '__all__'
        fields = ('id', 'name', 'slug',  'description', 'images' )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        task = Kitchen.objects.create(title=validated_data.get('title', 'no-title'),
                                   user_id=1)
        for image_data in images_data.values():
            KitchenGallary.objects.create(task=task, image=image_data)
        return task
#-------------------------------------------------------------------


#Блюда----------------------------------
class DishesGallarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishesGallary
        fields = ('image',)



class DishesSerializer(serializers.ModelSerializer):

    images = DishesGallarySerializer( many=True)
    class Meta:
        model = Dishes
        #fields = '__all__'
        fields = ('id', 'name', 'slug',  'description', 'images' )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        task = Dishes.objects.create(title=validated_data.get('title', 'no-title'),
                                   user_id=1)
        for image_data in images_data.values():
            DishesGallary.objects.create(task=task, image=image_data)
        return task
#-------------------------------------------------------------------

class DishFormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishFormat
        fields = ('pos', 'dish')
        depth = 2

class ProductSerializer(serializers.ModelSerializer):
    """
       Структура описавает модель события(мероприятиятия).
       Единица продажи.
    """
    dishes = DishFormatSerializer(many=True, read_only=True)
    kitchen = KitchenSerializer(read_only=True)
    #image_url = serializers.SerializerMethodField()
    #images = serializers. ('json',DishesGallary.image.all())
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'kitchen', 'dishes',
                  'slug', 'description', 'dateofevent', 'duration',
                  'quantity', 'price', 'stock', 'image', 'available')

        depth = 3

