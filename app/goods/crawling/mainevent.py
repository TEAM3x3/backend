import os
import re
import urllib

from django.core.files import File
from django.db import DataError
from selenium.common.exceptions import NoSuchElementException

from config.settings.base import MEDIA_ROOT
