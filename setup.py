
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='self-driving-desktop',
    version='0.0.3',
    author='Hofstadter, Inc.',
    author_email='support@hofstadter.io',
    description='Desktop Automation Framework. Drive your keyboard and mouse with text files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hofstadter-io/self-driving-desktop',
    packages=setuptools.find_packages(),
    classifiers=[],
    keywords=['desktop automation'],
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    sdd=self_driving_desktop:drive
    ''',
)
