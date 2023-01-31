from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme:
    description = readme.read()

setup(
    name='baidu_translate',
    version='0.0.1',
    packages=find_packages(),
    license='Unlicense',
    author='tq_xyy',
    author_email='17097231932@163.com',
    url='https://github.com/17097231932/baidu-translate/',
    description='一个免费, 高效, 简洁百度翻译接口',
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=['aiohttp', 'pycryptodome'],
    project_urls={
        'Documentation': 'https://github.com/17097231932/baidu-translate#readme',
        'Code': 'https://github.com/17097231932/baidu-translate',
        'Issue tracker': 'https://github.com/17097231932/baidu-translate/issues',
    },
    zip_safe=False,
)
