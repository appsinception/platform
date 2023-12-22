import json
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

from nalgonda.persistence.agency_config_storage_interface import AgencyConfigStorageInterface
from nalgonda.settings import settings

# Initialize FireStore
if settings.google_credentials:
    cred_json = json.loads(settings.google_credentials)
    cred = credentials.Certificate(cred_json)
    firebase_admin.initialize_app(cred)


class AgencyConfigFirestoreStorage(AgencyConfigStorageInterface):
    def __init__(self, agency_id: str):
        self.db = firestore.client()
        self.agency_id = agency_id
        self.collection_name = "agency_configs"
        self.document = self.db.collection(self.collection_name).document(agency_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No special action needed on exiting the context.
        pass

    def load(self):
        return self.document.get().to_dict()

    def save(self, data: dict[str, Any]):
        self.document.set(data)