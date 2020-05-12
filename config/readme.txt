# API проекта StudioMyka
# django
# rest api
Проект, реализующий Rest API, для ивент магазина.
Реализовано:

- создание события;
- наполнение события описанием, фото, дата проведения, стоимость и количество мест участников;
- заказ и бронирование;
- галерея картинок;
- фильтрация по типу события, календарю, стоимости;
- уведомление на почту покупателя;
- карзина покупок;
- администрирование магазина через модифицированный дашборд django;
- регистрация через соц сети;
- эквайринг Райфайзен банка.






в пакете 'sortedm2m' модуль fields.py  метод _add_item(....,**kwargs) добавить!!!


в пакете drf_yasq закомменитровать импорты
#from packaging.version import Version
#if Version(rest_framework.__version__) < Version('3.10'):
#    from rest_framework.schemas.generators import SchemaGenerator
#    from rest_framework.schemas.inspectors import get_pk_description
#else:


для регистрации через соц.сети. доступны FB, VK, Instagram
url для каждой из них
/account/social/login/facebook
/account/social/login/vk-oauth2
/account/social/token/instagram
