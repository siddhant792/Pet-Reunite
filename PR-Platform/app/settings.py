"""
Settings Module
"""

import os

from google.cloud import firestore, storage

PROJECT_ID = os.environ.get("PROJECT_ID", "pet-reunite-410804")
FS_CLIENT = firestore.Client(project=PROJECT_ID)
STORAGE_CLIENT = storage.Client(project=PROJECT_ID)
