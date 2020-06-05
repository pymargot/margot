from distutils.core import setup

setup(
    name = 'margot',         # How you named your package folder (MyLib)
    packages = ['margot'],   # Chose the same as "name"
    version = '0.0.1',      # Start with a small number and increase it with every change you make
    license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'simple to use, batteries included, tools for quantitative trading.',   # Give a short description about your library
    author = 'Rich Atkinson',                   # Type in your name
    author_email = 'rich@airteam.com.au',      # Type in your E-Mail
    url = 'https://github.com/atkinson/margot',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/atkinson/margot/archive/v_0.0.1.tar.gz',    # I explain this later on
    keywords = ['quant', 'trading', 'systematic'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
            'numpy',
            'pandas',
            'scipy',
            'pyfolio',
            'trading-calendars'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: apache-2.0',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)