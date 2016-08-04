from django.db import models
from django.template.defaultfilters import slugify


class GZH(models.Model):

    name = models.CharField(max_length=50, unique=True)
    weixin_id = models.CharField(max_length=50, unique=True)
    head_pic = models.URLField()
    qr_code = models.URLField()
    introduction = models.CharField(max_length=500)
    verify_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # gzh_paper_url = models.URLField()

    def __str__(self):
        return self.weixin_id


class Article(models.Model):
    gzh = models.ForeignKey(GZH)
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.CharField(max_length=30)
    source_url = models.URLField()
    video_url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # slug = models.SlugField()
    #
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.gzh)
    #     super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


