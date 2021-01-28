# This snippet removes html comments from a stream
#
# oneliner lambda rules !
from bs4 import BeautifulSoup, Comment

#..."soup" contains, well.. the soup object
[comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]
# now comments are gone
