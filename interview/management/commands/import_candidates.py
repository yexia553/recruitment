import csv
from django.core.management import BaseCommand
from interview.models import Candidate


class Command(BaseCommand):
    """
    利用django自带的management command功能实现从csv文件导入候选人
    """
    help = '从csv文件导入候选人列表'

    def add_arguments(self, parser):
        """
        定义参数形式，这里用的事长命令参数的格式，命令阳历如下：
        python manage.py import_candidates --path /file/to/候选人.csv
        :param parser:
        :return:
        """
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        """
        定义实际处理逻辑
        :param args:
        :param kwargs:
        :return:
        """
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                # 每一行数据都一个候选人信息，在数据库中创建一条数据
                candidate = Candidate.objects.create(
                    username=row[0],
                    city=row[1],
                    phone=row[2],
                    bachelor_school=row[3],
                    major=row[4],
                    degree=row[5],
                    test_score_of_general_ability=row[6],
                    paper_score=row[7],
                )
                print(candidate)