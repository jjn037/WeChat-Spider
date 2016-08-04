from django.core.management.base import BaseCommand
from wechat_gzh import wechat_spider02


class Command(BaseCommand):
    def handle(self, *args, **options):
        # wechat_spider02.main()
        print('hello')

