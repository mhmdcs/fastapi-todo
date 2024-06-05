from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id, models.Task.title.contains(search)).limit(limit).offset(skip).all()
   return tasks

@router.get("/{id}", response_model=schemas.TaskResponse)
def get_task(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id).first() # filter is the equivalent of WHERE on a SQL query statement
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} was not found")
    
    if current_user.id != task.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    return task

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_task = models.Task(owner_id=current_user.id, **task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id == id)

    quered_task = task_query.first()

    if quered_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id {id} does not exist")
    
    if current_user.id != quered_task.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    task_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id==id)
    
    updated_task = task_query.first()

    if updated_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id {id} does not exist")
    
    if current_user.id != updated_task.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    task_query.update(task.dict(), synchronize_session=False)
    db.commit()

    return task_query.first()

@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_task_status(id: int, status: schemas.TaskStatus, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.id==id)
    
    updated_task = task_query.first()

    if updated_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id {id} does not exist")
    
    if current_user.id != updated_task.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    task_query.update({'done': status.done}, synchronize_session=False)
    db.commit()

    message = "task marked as done" if status.done else "task marked as undone"
    
    return {"status": message}

@router.post("/share")
def share_tasks(task_share: schemas.TaskShare, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # buggy implemenetation, did not have enough time to debug / think this one through since time is tight

    user_to_share = db.query(models.User).filter(models.User.email == task_share.email).first()
    if not user_to_share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_to_share.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot share tasks with yourself")

    if task_share.share:
        current_user_tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
        for task in current_user_tasks:
            new_task = models.Task(title=task.title, content=task.content, done = task.done, owner_id=user_to_share.id)
            db.add(new_task)
        db.commit()
        return {"message": "Tasks shared successfully"}

    else:
        task_ids_to_unshare = db.query(models.Task.id).filter(models.Task.owner_id == current_user.id).subquery()
        
        db.query(models.Task).filter(
            models.Task.owner_id == current_user.id,
            models.Task.id.in_(task_ids_to_unshare)
        ).delete(synchronize_session=False)
        db.commit()
        return {"message": "Tasks unshared successfully"}