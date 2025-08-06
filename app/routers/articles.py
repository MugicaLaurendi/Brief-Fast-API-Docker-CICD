from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models import Articles
from app.schemas import ArticleCreate, ArticleRead, ArticleUpdate
from app.models import get_session
from sqlmodel import select
from sqlmodel import Session

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/articles/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate, db: Session = Depends(get_session)):
    db_item = Articles.from_orm(article)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/articles/", response_model=List[ArticleRead])
def list_articles(db: Session = Depends(get_session)):
    return db.exec(select(Articles)).all()

@router.get("/articles/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articles non trouvé")
    return item

@router.put("/articles/{article_id}", response_model=ArticleRead)
def update_article(article_id: int, article: ArticleCreate, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articles non trouvé")
    for k, v in article.model_dump().items():
        setattr(item, k, v)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.patch("/articles/{article_id}", response_model=ArticleRead)
def patch_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articles non trouvé")
    update_data = article.model_dump(exclude_none=True)
    for k, v in update_data.items():
        setattr(item, k, v)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_session)):
    item = db.get(Articles, article_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articles non trouvé")
    db.delete(item)
    db.commit()
