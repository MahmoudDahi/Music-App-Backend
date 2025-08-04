import uuid
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader

from models.song import Song

router = APIRouter()

# Configuration       
cloudinary.config( 
    cloud_name = "duifiib3g", 
    api_key = "851967516178976", 
    api_secret = "0zo5lcoVgm_0a-R7-1hfh1tI69k", # Click 'View API Keys' above to copy your API secret
    secure=True
)

@router.post('/upload',status_code=201)
def upload_song(song: UploadFile= File(...),
                thumbnail: UploadFile = File(...),
                artist:str = Form(...),
                song_name: str = Form(...),
                color: str = Form(...),
                db: Session = Depends(get_db),
                userID= Depends(auth_middleware)):
    song_uuid= str(uuid.uuid4())
    song_res= cloudinary.uploader.upload(song.file,resource_type="auto",folder=f'songs/{song_uuid}')
    thumbnail_res= cloudinary.uploader.upload(thumbnail.file,resource_type="image",folder=f'songs/{song_uuid}')
    
    new_song = Song(
        id=song_uuid,
        song_name=song_name,
        artist=artist,
        hex_code=color,
        song_url=song_res['url'],
        thumbnail_url=thumbnail_res['url'],
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return new_song

@router.get('/list')
def fetch_song_list(db : Session=Depends(get_db),userID = Depends(auth_middleware)):
    songs_list = db.query(Song).all()
    return songs_list
