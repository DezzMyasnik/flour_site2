from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
    title = 'LastNews'
    link = '/blog/'
    description = 'Последние новости студии'

    def items(self):
        return Post.objects.all().order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

