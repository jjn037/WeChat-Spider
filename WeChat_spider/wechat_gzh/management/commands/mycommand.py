from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # wechat_spider02.main()
        print('hello')

