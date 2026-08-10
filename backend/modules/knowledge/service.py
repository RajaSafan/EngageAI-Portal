from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from uuid import UUID

from modules.knowledge.models import (
    KnowledgeBase,
    SourceType,
    ProcessingStatus,
)

from core.blob_storage import (
    upload_pdf,
    upload_text,
    upload_url,
    delete_blob,
)


# ============================================================
# Knowledge Upload (Azure Blob Storage + Database)
# ============================================================


def add_text_source(
    db: Session,
    organization_id,
    content: str
):

    blob_url = upload_text(content)


    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.Text,
        source_path=blob_url,
        processing_status=ProcessingStatus.Completed,
    )


    db.add(kb)
    db.commit()
    db.refresh(kb)


    return kb



def add_url_source(
    db: Session,
    organization_id,
    url: str
):

    blob_url = upload_url(url)


    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.URL,
        source_path=blob_url,
        processing_status=ProcessingStatus.Completed,
    )


    db.add(kb)
    db.commit()
    db.refresh(kb)


    return kb



def add_pdf_source(
    db: Session,
    organization_id,
    file: UploadFile
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )


    blob_url = upload_pdf(file)


    kb = KnowledgeBase(
        organization_id=organization_id,
        source_type=SourceType.PDF,
        source_path=blob_url,
        processing_status=ProcessingStatus.Completed,
    )


    db.add(kb)
    db.commit()
    db.refresh(kb)


    return kb



# ============================================================
# Knowledge Listing
# ============================================================


def get_organization_knowledge(
    db: Session,
    organization_id
):

    return (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.organization_id == organization_id
        )
        .order_by(
            KnowledgeBase.created_at.desc()
        )
        .all()
    )



# ============================================================
# Delete Knowledge Source
# ============================================================


def delete_knowledge_source(
    db: Session,
    knowledge_base_id: str,
    organization_id
):

    kb = (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.knowledge_base_id == UUID(knowledge_base_id),
            KnowledgeBase.organization_id == organization_id
        )
        .first()
    )


    if not kb:

        raise HTTPException(
            status_code=404,
            detail="Knowledge source not found"
        )


    # Delete file from Azure Blob Storage

    if kb.source_path:

        try:

            delete_blob(
                kb.source_path
            )

        except Exception:

            pass



    # Delete record from database

    db.delete(kb)

    db.commit()


    return {
        "message": "Knowledge source deleted successfully"
    }