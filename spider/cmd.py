# conding = utf-8
from . import Spider
import argparse


def get_args():
    desc = '一个可以自动抓取知乎日报热门文章及文章中的图片的爬虫'
    parser = argparse.ArgumentParser(
        description=desc)
    parser.add_argument('path',
                        nargs='?',
                        metavar='PATH',
                        default=None,
                        const=None,
                        help='你想放置抓取结果的文件夹(默认=./zhihu_daily)')
    args = parser.parse_args()
    return args.path


def main():
    path = get_args()
    Spider(path)
