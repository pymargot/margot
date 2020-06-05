
to install, simply pip install margot

margot needs some environment variables, depending on what you're going to be doing.

These can be passed in at runtime using a dictionary (env={}), or made available via the system environment.

For now, we'll use the system environment.

Firstly, margot needs to know where you would like to store your hdf5 data files:

DATA_CACHE = '~/.hdf5/'

If you're getting data from Alphavantage, you'll need an API key:

ALPHAVANTAGE_API_KEY = 'your-key'