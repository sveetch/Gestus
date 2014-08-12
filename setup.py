from setuptools import setup, find_packages

setup(
    name='Gestus',
    version=__import__('gestus').__version__,
    description=__import__('gestus').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='dthenon@emencia.com',
    url='http://pypi.python.org/pypi/Gestus',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'djangorestframework >= 2.3',
        'autobreadcrumbs >= 1.0',
        'django-braces>=1.2.0,<1.4',
    ],
    include_package_data=True,
    zip_safe=False
)