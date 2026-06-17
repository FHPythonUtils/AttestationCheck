import requests_cache
from platformdirs import PlatformDirs

dirs = PlatformDirs("attestationcheck", "fredhappyface")


session = requests_cache.CachedSession(dirs.user_cache_dir)
