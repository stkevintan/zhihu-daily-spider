# encoding utf-8
import os


class FsWriter:
    def __init__(self, path=None):
        self.path = path or os.path.join(os.getcwd(), 'zhihu_daily')
        if not os.path.exists(self.path):
            os.mkdir(self.path)  # 如果不存在

    def _get_path(self, path, base=None):
        return os.path.join(base or self.path, path)

    def write_summary(self, source=[]):
        # write summary
        titles = ['%s: %s\n' % (topic.get('id'), topic.get('title')) for topic in source]
        fp = open(self._get_path('summary.txt'), 'w')
        fp.writelines(titles)
        fp.close()

    def write_seperator(self, fp, character='#', num=81):
        fp.write(character * num + '\n')

    def write_content(self, source={}):
        # write content
        base = self._get_path(source.get('id', 'Unknown'))
        if not os.path.exists(base):
            os.mkdir(base)  # 以id名创建文件夹
        fp = open(self._get_path(source.get('title'), base), 'w')
        # 写背景
        if 'background' in source:
            bg = source['background']
            fp.write('相关信息：%s\n' % bg.get('title'))
            fp.write('链接：%s\n' % bg.get('link'))
        unknown = '未知'
        # 写内容
        for question in source.get('question'):
            # 分隔符
            self.write_seperator(fp)
            # 原问题和作者信息
            fp.write('原问题： %s\n' % (question.get('title') or unknown))  # %比or优先级高
            fp.write('作者： %s\n' % (question.get('author') or unknown))
            fp.write('作者简介： %s\n' % (question.get('bio') or unknown))
            # 分隔符
            self.write_seperator(fp, '=')

            # 正文
            if 'content' in question:
                fp.write(question['content'] + '\n')
            else:
                fp.write('内容获取失败\n')
            # 空行
            fp.write('\n' * 4)
        fp.close()

    def write_image(self, source={}):
        base = self._get_path(source.get('id', 'Unknown'))
        if not os.path.exists(base):
            os.mkdir(base)  # 以id名创建文件夹
        fp = open(self._get_path(source['name'], base), 'wb')
        fp.write(source['data'])
