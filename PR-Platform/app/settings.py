"""
Settings Module
"""

import os

from google.cloud import firestore

PROJECT_ID = os.environ.get("PROJECT_ID")
FS_CLIENT = firestore.Client()
