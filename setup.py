from setuptools import setup, find_packages


setup(
    name = "simplepages",
    version = '0.54.0',
    description = "A basic site structure and pages app",
    keywords = "django, cms, pages, contentmanagement",
    author = "Alex Kamedov",
    author_email = "alex@kamedov.ru",
    url = "git@3128.ru:repos/django-snippets.git",
    license = "New BSD License",
    platforms = ["any"],
    classifiers = ["Development Status :: stable",
                   "Environment :: Web Environment",
                   "Framework :: Django",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Utilities"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data = {
        'linker': [
            'locale/*/LC_MESSAGES/*.*',
            'templates/*',
            'media/*',
        ],
    },
)

