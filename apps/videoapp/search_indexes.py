from haystack import indexes

from videoapp.models import *


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引内容，document和use_template都为true
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):  # 索引查询的模型类
        return Course

    def index_queryset(self, using=None):
        print("xxxxxxx")
        return self.get_model().objects.all()
