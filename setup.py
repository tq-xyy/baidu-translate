from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme:
    description = readme.read()

setup(
    name='baidu-translate-api',
    version='1.0.0',
    packages=find_packages(),
    license='Unlicense',
    author='tq_xyy',
    author_email='m17097231932@163.com',
    url='https://github.com/tq-xyy/baidu-translate/',
    description='一个免费, 高效, 简洁百度翻译接口',
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=['httpx', 'pycryptodome'],
    project_urls={
        'Documentation': 'https://github.com/tq-xyy/baidu-translate#readme',
        'Code': 'https://github.com/tq-xyy/baidu-translate',
        'Issue tracker': 'https://github.com/tq-xyy/baidu-translate/issues',
    },
    zip_safe=False,
)
