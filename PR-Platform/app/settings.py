"""
Settings Module
"""

import os

from google.cloud import firestore

PROJECT_ID = os.environ.get("PROJECT_ID", "pet-reunite-410804")
FS_CLIENT = firestore.Client(PROJECT_ID)
