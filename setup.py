from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    description = readme.read()

setup(
    name='baidu_translate',
    version='1.0.0',
    packages=['baidu_translate'],
    license='Public Domain',
    author='tq_xyy',
    author_email='17097231932@163.com',
    url='https://github.com/17097231932/baidu-translate/',
    description='一个免费, 高效, 简洁百度翻译接口',
    long_description=description,
    requires=['reuqests'],
)
