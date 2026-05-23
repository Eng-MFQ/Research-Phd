from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

from models.Models import AIAgentModel


def init_firebase():
    cred = credentials.Certificate(f"./whilearn/firebase/service_account_key.json")
    firebase_admin.initialize_app(cred)


def available_credit_balance(user_id):
    db = firestore.client()
    users_ref = db.collection("GPTsUsers").document(user_id)
    user_doc = users_ref.get()

    if user_doc.exists:
        credit_balance = user_doc.to_dict().get("creditBalance", 0)

        if credit_balance <= 0:
            return False

        return True

    return False




def getAiContentUser(email):
    db = firestore.client()
    docs = (
        db.collection("ContentUserCollection")
        .where(filter=FieldFilter('userId', '==', email))
        .get()
    )
    return docs


def getGPT(gptId):
    db = firestore.client()
    docs = (
        db.collection("GPTs")
        .where(filter=FieldFilter('aiAgentId', '==', gptId))
        .get()
    )
    return docs


def increaseContentPosts(doc):
    doc.reference.update({"postsNumber": firestore.Increment(1)})


def getKey(doc):
    return doc.get("openaiKey")


def addUsage(userId, promptType, usage, response):
    client = {
        'userId': userId,
        'type': promptType,
        "prompt_tokens": usage.prompt_tokens,
        "response": f"{response}",
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "timestamp": datetime.now()
    }
    firestore.client().collection("ContentUsageCollection").document().set(client)
