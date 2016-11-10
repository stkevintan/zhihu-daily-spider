from setuptools import setup, find_packages

setup(
    name='zhihu-spider',
    author='Kevin Tan',
    description='一个可以自动抓取知乎日报热门文章及文章中的图片的爬虫',
    version='0.1',
    license='MIT',
    install_requires=['beautifulsoup4>=4.5', 'argparse>=1.4.0'],
    packages=find_packages("spider"),
    entry_points={
        'console_scripts': [
            'zhihu-spider = spider.cmd:main'
        ]
    }
)
