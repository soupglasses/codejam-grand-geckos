import sys

from grand_geckos.features import say_hello

print(say_hello(" ".join(sys.argv[1:]) or "World"))
