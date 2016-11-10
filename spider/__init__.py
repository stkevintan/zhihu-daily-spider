# conding = utf-8

from .request import RequestWrap
from .writer import FsWriter

import re
import threading


class Spider:
    url = 'http://daily.zhihu.com'

    def __init__(self, desc=None):
        self.raw_body = {}  # 储存网页名和对应的网页原始字符串
        self.url.rstrip('/')
        self.writer = FsWriter(desc)
        print('spider begin...')
        self.request = RequestWrap()
        self.topics = []
        self.get_index()
        self.get_details()

    def get_index(self):
        result = self.request.get(self.url)
        topic_blocks = result.select('.main-content-wrap .box')
        for topic_block in topic_blocks:
            topic = {
                'title': self.get_text(topic_block),
                'id': re.search(r'\d+$', topic_block.a.get('href')).group(),
                'image': topic_block.img.get('src')
            }
            self.topics.append(topic)
        self.writer.write_summary(self.topics)

    @staticmethod
    def get_text(block=None):
        return block.get_text() if block is not None else None

    @staticmethod
    def get_first(blocks=[]):
        return blocks[0] if blocks.__len__() > 0 else None

    def get_detail(self, url, base):
        print('going to fetch data from %s' % url)
        html_detail = self.request.get(url)
        result = base.copy()
        # 获得相关新闻信息
        background_block = self.get_first(html_detail.select('.headline .headline-background'))
        if background_block:
            result['background'] = {
                'title': background_block.find(class_='heading-content').get_text(),
                'link': background_block.find('a').get('href')
            }

        result['question'] = []
        # 获得回答，去掉最后的下载APP提示
        question_blocks = html_detail.select('.content-inner > .question')
        for question_block in question_blocks:
            cur_question = {}
            meta_block = self.get_first(question_block.select('.answer > .meta'))
            content_block = self.get_first(question_block.select('.answer > .content'))

            # 获取元信息
            if meta_block:
                cur_question['title'] = self.get_text(meta_block.find(class_='question-title'))
                cur_question['author'] = self.get_text(meta_block.find(class_='author'))
                cur_question['bio'] = self.get_text(meta_block.find(class_='bio'))

            # 获取正文信息
            if content_block:
                cur_question['content'] = self.get_text(content_block)
                cur_question['image_list'] = [img_block.get('src') for img_block in content_block.find_all('img')]

            content = cur_question.get('content')
            if content and content.find('客官，这篇文章有意思吗？') == -1:
                result['question'].append(cur_question)
                if cur_question.get('image_list', []).__len__() > 0:
                    # 获得图片数据
                    for img_url in cur_question['image_list']:
                        # 多线程下载图片
                        print('start downloading image from %s' % img_url)
                        t = threading.Thread(target=self.get_image, args=[img_url, base])
                        t.start()
        self.writer.write_content(result)
        print('one topic(id = %s) has completed' % result.get('id'))

    def get_image(self, url, base):
        html_image = self.request.get(url, headers={"Host": "pic2.zhimg.com"}, utf8=False)
        print('downloading has been complete')
        result = base.copy()
        result['data'] = html_image
        # 获取图片名称
        result['name'] = re.search(r'\w+(?:\.\w+)?$', url).group()
        self.writer.write_image(result)

    def get_details(self):
        for topic in self.topics:
            topic_id = topic.get('id')
            topic_title = topic.get('title')
            url = self.url + '/story/' + topic_id
            # 使用多线程
            t = threading.Thread(target=self.get_detail, args=[url, {'title': topic_title, 'id': topic_id}])
            t.start()


if __name__ == '__main__':
    Spider()
