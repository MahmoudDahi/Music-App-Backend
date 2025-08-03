import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader

router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = "duifiib3g", 
    api_key = "851967516178976", 
    api_secret = "0zo5lcoVgm_0a-R7-1hfh1tI69k", # Click 'View API Keys' above to copy your API secret
    secure=True
)

@router.post('/upload')
def upload_song(song: UploadFile= File(...),
                thumbnail: UploadFile = File(...),
                artist:str = Form(...),
                song_name: str = Form(...),
                color: str = Form(...),
                db: Session = Depends(get_db),
                userID= Depends(auth_middleware),):
    song_uuid= str(uuid.uuid4())
    song_res= cloudinary.uploader.upload(song.file,resource_type="auto",folder=f'songs/{song_uuid}')
    print(song_res)
    thumbnail_res= cloudinary.uploader.upload(thumbnail.file,resource_type="image",folder=f'songs/{song_uuid}')
    print(thumbnail_res)

    return 'ok'
