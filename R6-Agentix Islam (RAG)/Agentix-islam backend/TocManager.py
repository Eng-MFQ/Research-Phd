from datetime import datetime
from typing import Iterable, Dict, Any, Optional, List
import json

import firebase_admin
from fastapi import HTTPException
from firebase_admin import credentials, firestore
# Upload pages
import time
import random
from typing import List, Dict, Iterable, Optional
from google.api_core.exceptions import Aborted, DeadlineExceeded, ServiceUnavailable
from google.cloud.firestore_v1 import FieldFilter

from APIs.AiUtilis import calculate_gemini_cost
from models.FirebaseHelper import init_firebase

cred = credentials.Certificate("./whilearn/Agentix-Islam/firebase/agentix-islam-service_account.json")
agentic_app = firebase_admin.initialize_app(cred, name='agentix')


def _chunked(iterable: Iterable[Dict[str, Any]], size: int) -> Iterable[List[Dict[str, Any]]]:
    """Yield lists of at most `size` items from `iterable`."""
    batch: List[Dict[str, Any]] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def upload_toc(
        book_id: str,
        toc_items: Iterable[Dict[str, Any]],
        *,
        cred_path: Optional[str] = None,
        project_id: Optional[str] = None,
        merge: bool = True,
        batch_size: int = 500
) -> Dict[str, Any]:
    """
    Upload a TOC list to Firestore under books/{book_id}/toc.

    - book_id: your book document ID.
    - toc_items: iterable of dicts like:
        {
          "id": "item_1",
          "level": 1,
          "title": "مقدمة الطبعة الجديدة",
          "startPage": 17,
          "endPage": 20,
          "parentId": None,
          "pathIds": ["item_1"],
          "pathTitles": ["مقدمة الطبعة الجديدة"],
          "is_confident": True
        }
    - merge: if True, upserts documents; if False, overwrites completely.

    Returns summary: {"book_id": ..., "written": N, "batches": B}
    """
    try:
        firebase_admin.get_app()
    except ValueError:
        init_firebase()
    db = firestore.client()
    col_ref = db.collection("books").document(book_id).collection("toc")

    total_written = 0
    batches = 0

    for group in _chunked(toc_items, batch_size):
        batch = db.batch()
        for entry in group:
            doc_id = entry.get("id")
            if not doc_id:
                # If missing, generate an auto ID but keep the entry as-is otherwise.
                doc_ref = col_ref.document()
            else:
                doc_ref = col_ref.document(str(doc_id))

            # Write the entry as-is. merge=True prevents duplicates on reruns.
            batch.set(doc_ref, entry, merge=merge)
        batch.commit()
        total_written += len(group)
        batches += 1

    return {"book_id": book_id, "written": total_written, "batches": batches}


# ---------- Convenience: load from a JSON file ----------

def upload_toc_from_file(
        book_id: str,
        json_path: str,
        *,
        cred_path: Optional[str] = None,
        project_id: Optional[str] = None,
        merge: bool = True,
) -> Dict[str, Any]:
    """
    Read a JSON array from `json_path` and upload to books/{book_id}/toc.
    """
    print(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        toc_list = json.load(f)
        if not isinstance(toc_list, list):
            raise ValueError("Expected a JSON array at the root.")
    return upload_toc(
        book_id,
        toc_list,
        cred_path=cred_path,
        project_id=project_id,
        merge=merge,
    )


def _chunk(lst: List[Any], n: int) -> List[List[Any]]:
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def get_book_information(my_book_id: str):
    db = firestore.client(agentic_app)
    col_name = "books"
    book_ref = db.collection(col_name).document(my_book_id)
    book_doc = book_ref.get()
    if book_doc.exists:
        return book_doc.to_dict()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"no such book {my_book_id}"
        )


def save_usage(collection: str, usage: dict, results: dict, model: str = "gemini-2.5-flash"):
    db = firestore.client(agentic_app)
    calculate_gemini_cost(usage, model)
    usage_ref = db.collection(collection)
    if usage:
        usage_doc_data = {
            **usage,
            **results,
            "timestamp": datetime.now()
        }
        usage_ref.add(usage_doc_data)


def save_conversation(question: str, answer: dict, book_id: str, user_id: str):
    db = firestore.client(agentic_app)
    conversation_ref = db.collection("conversation")
    doc_data = {
        "question": question,
        "answer": answer.get("answer", ""),
        "bookId": book_id,
        "userId": user_id,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    conversation_ref.add(doc_data)



async def find_page_scopes(book_id: str, page_number: int, book_part_number: int = 0) -> Dict[str, Any]:
    """
    Returns:
      {
        "page": int,
        "leaf": {"id","title","startPage","endPage","level"},
        "scopes_top_down": [ same shape as leaf, from root -> leaf ],
        "scopes_small_to_big": [ leaf -> ... -> root ]    # convenience order
      }
      or { "page": int, "leaf": None, "scopes_top_down": [] } if no section contains the page.
    """
    db = firestore.client(agentic_app)
    book_ref = db.collection("books").document(book_id).collection("parts").document(f"{book_part_number}")
    toc = book_ref.collection("toc")

    # 1) Find the smallest (deepest) section that contains `page`
    #    Query only uses one inequality (startPage <= page), then sorts to find the first match whose endPage >= page.
    #    Requires composite index: startPage DESC, level DESC on collectionGroup 'toc'.
    q = (
        toc.where("startPage", "<=", page_number)
        .order_by("startPage", direction=firestore.Query.DESCENDING)
        .order_by("level", direction=firestore.Query.DESCENDING)
        .limit(40)  # depth is usually small; bump if your TOC is unusual
    )

    leaf_snap = None
    for snap in q.stream():
        d = snap.to_dict() or {}
        if d.get("endPage") is not None and d["endPage"] >= page_number:
            leaf_snap = snap
            break

    if not leaf_snap:
        return {"book_id": book_id, "page": page_number, "leaf": None, "scopes_top_down": [],
                "scopes_small_to_big": []}

    leaf = leaf_snap.to_dict()
    leaf_node = {
        "id": leaf.get("id", leaf_snap.id),
        "title": leaf.get("title"),
        "startPage": leaf.get("startPage"),
        "endPage": leaf.get("endPage"),
        "level": leaf.get("level"),
        "book_part_number": book_part_number,
    }

    # 2) Build scopes from ancestors (top→down). Prefer pathIds (already ordered).
    scopes_top_down: List[Dict[str, Any]] = []
    path_ids: Optional[List[str]] = leaf.get("pathIds")

    if path_ids:
        # Firestore 'in' supports up to 10 values — fetch in chunks, then re-order per path_ids.
        id_to_doc: Dict[str, Dict[str, Any]] = {}
        for batch in _chunk(path_ids, 10):
            for s in toc.where("id", "in", batch).stream():
                id_to_doc[s.to_dict().get("id", s.id)] = s.to_dict()

        for pid in path_ids:
            d = id_to_doc.get(pid)
            if d:
                scopes_top_down.append({
                    "id": d.get("id"),
                    "title": d.get("title"),
                    "startPage": d.get("startPage"),
                    "endPage": d.get("endPage"),
                    "level": d.get("level"),
                    "book_part_number": book_part_number,
                })

    else:
        # Fallback: climb via parentId
        # Build bottom-up, then reverse.
        chain: List[Dict[str, Any]] = []
        current = leaf
        seen = set()
        while current and current.get("id") not in seen:
            seen.add(current.get("id"))
            chain.append({
                "id": current.get("id"),
                "title": current.get("title"),
                "startPage": current.get("startPage"),
                "endPage": current.get("endPage"),
                "level": current.get("level"),
                "book_part_number": book_part_number,
            })
            parent_id = current.get("parentId")
            if not parent_id:
                break
            # Using an equality query in case Firestore doc-id != field "id"
            parent_snaps = list(toc.where("id", "==", parent_id).limit(1).stream())
            current = parent_snaps[0].to_dict() if parent_snaps else None

        scopes_top_down = list(reversed(chain))

    # 3) Convenience order (smallest→largest)
    scopes_small_to_big = list(reversed(scopes_top_down))

    return {
        "page": page_number,
        "leaf": leaf_node,
        "scopes_small_to_big": scopes_small_to_big,
    }


def get_range(book_id: str, page: int):
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(f"../whilearn/firebase/service_account_key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    toc = db.collection('books').document(book_id).collection('toc')
    q = toc.where('startPage', '==', page)
    docs = list(q.stream())
    results = []
    for d in docs:
        results.append(d.to_dict())
        print(d.to_dict()["startPage"])
        print(d.to_dict()["endPage"])
        print(d.to_dict()["endPage"] - d.to_dict()["startPage"])
        print(d.to_dict()["level"])
        print("----")
    return results


def _chunked(seq: List[Dict], size: int) -> Iterable[List[Dict]]:
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def upload_pages_to_firestore(
        book_id: str,
        pages: List[Dict],
        batch_size: int = 450,
        overwrite: bool = False,
        collection_root: str = "books",
        max_retries: int = 5,
        jitter_seconds: float = 0.2,
) -> int:
    """
    يرفع صفحات كتاب (قائمة JSON) إلى Firestore تحت:
        /books/{book_id}/pages/{page_number}

    Args:
        book_id: معرف الكتاب.
        pages: قائمة من القواميس، كل عنصر يحتوي على الأقل:
               {"page_number": int, "page_content": str, "is_missing": bool}
        batch_size: حجم الدفعة (<= 500).
        overwrite: إذا True يستخدم set(.., merge=False) فيستبدل الوثيقة بالكامل.
                   إذا False (الموصى به) يستخدم merge=True للتحديث دون استبدال كامل.
        collection_root: اسم مجموعة الجذر ("books" افتراضيًا).
        max_retries: عدد محاولات إعادة الإرسال عند الأخطاء القابلة لإعادة المحاولة.
        jitter_seconds: اهتزاز زمني صغير لتقليل تضارب الطلبات.

    Returns:
        عدد الوثائق المكتوبة بنجاح.
    """
    if batch_size < 1 or batch_size > 500:
        raise ValueError("batch_size must be between 1 and 500")

    # تأكد من تهيئة Firebase
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(f"../whilearn/firebase/service_account_key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    col_ref = db.collection(collection_root).document(book_id).collection("pages")

    written = 0

    # تحقق بسيط من المدخلات
    cleaned_pages = []
    for p in pages:
        if "page_number" not in p:
            raise ValueError("Each page dict must include 'page_number'.")
        cleaned_pages.append(p)

    for chunk in _chunked(cleaned_pages, batch_size):
        attempt = 0
        while True:
            try:
                batch = db.batch()
                for page in chunk:
                    page_num = page["page_number"]
                    if page_num is None:
                        raise ValueError("page_number cannot be None")

                    # استخدم page_number كمعرّف الوثيقة لسهولة القراءة/التحديث لاحقًا
                    doc_ref = col_ref.document(str(page_num))

                    data = {
                        "page_number": page["page_number"],
                        "page_content": page.get("page_content", ""),
                    }

                    # يمكنك إضافة حقول إضافية هنا مثل created_at/updated_at باستخدام cloud functions
                    if overwrite:
                        batch.set(doc_ref, data, merge=False)
                    else:
                        batch.set(doc_ref, data, merge=True)

                # تنفيذ الكتابة
                batch.commit()
                written += len(chunk)
                # فاصل صغير اختياري لتجنّب ضغط مرتفع
                time.sleep(random.uniform(0, jitter_seconds))
                break  # خرجنا من حلقة retry لهذه الدفعة

            except (Aborted, DeadlineExceeded, ServiceUnavailable) as e:
                attempt += 1
                if attempt > max_retries:
                    raise RuntimeError(
                        f"Failed to commit a batch after {max_retries} retries"
                    ) from e
                # backoff أُسّي مع اهتزاز
                sleep_s = (2 ** (attempt - 1)) + random.uniform(0, jitter_seconds)
                time.sleep(sleep_s)

    return written


def upload_page_content_to_db(path: str, fiqh_book_id: str):
    # حمّل ملف الصفحات الكبير
    with open(path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    count = upload_pages_to_firestore(
        book_id=fiqh_book_id,
        pages=pages,
        batch_size=450,  # < 500 للتوافق مع حدود Firestore
        overwrite=False  # استخدم merge لتحديث آمن دون استبدال كامل
    )

    print(f"تم رفع {count} صفحة بنجاح.")


async def get_pages_in_range(book_id: str, start_page: int, end_page: int, book_part: int = 0):
    db = firestore.client(agentic_app)
    col = db.collection("books").document(book_id).collection("parts").document(f"{book_part}").collection("pages")
    q = (col.where(filter=FieldFilter("page_number", ">=", start_page))
         .where(filter=FieldFilter("page_number", "<=", end_page))
         .order_by("page_number"))
    return [{**d.to_dict()} for d in q.stream()]
