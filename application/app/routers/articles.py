from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import List

from app.models import Articles
from app.database_connection import get_session
from app.schemas import ArticleCreate, ArticleRead, ArticleUpdate
from app.security import require_role



router = APIRouter(prefix="/articles", tags=["Articles"])



# ===========================
#   CRUD COMPLET DES ARTICLES
# ===========================


# Creer un article
@router.post("/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role([1]))])
def create_article(article: ArticleCreate, db: Session = Depends(get_session)):
    db_item = Articles.from_orm(article)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Lire tous les articles
@router.get("/", response_model=List[ArticleRead], dependencies=[Depends(require_role([1,2,3]))])
def list_articles(db: Session = Depends(get_session)):
    return db.exec(select(Articles)).all()


# Lire un article par ID
@router.get("/{article_id}", response_model=ArticleRead, dependencies=[Depends(require_role([1,2,3]))])
def get_article(article_id: int, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return item


# Modifier un article
@router.put("/{article_id}", response_model=ArticleRead, dependencies=[Depends(require_role([1]))])
def update_article(article_id: int, article: ArticleCreate, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    for k, v in article.model_dump().items():
        setattr(item, k, v)
    db.add(item)
    db.commit() 
    db.refresh(item)
    return item


# Mettre à jour partiellement un article
@router.patch("/{article_id}", response_model=ArticleRead, dependencies=[Depends(require_role([1,2]))])
def patch_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    update_data = article.model_dump(exclude_none=True)
    for k, v in update_data.items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# Supprimer un article
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role([1]))])
def delete_article(article_id: int, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    db.delete(item)
    db.commit()
