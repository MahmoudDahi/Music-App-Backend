from fastapi import Header ,HTTPException
from core.utils import secretKey
import jwt


def auth_middleware(x_auth_token= Header()):
    try:
        if not x_auth_token:
            raise HTTPException(401,'No auth Token, Access Denied! ') 
        verify_token = jwt.decode(x_auth_token,secretKey,algorithms=['HS256'])
        
        if not verify_token:
            raise HTTPException(401,'Invalid token!')
        user_id = verify_token.get('id')    
        return {"user_id":user_id,"token":x_auth_token}
    except jwt.PyJWKError:
        raise HTTPException(401,'Token is not Valid, Authorization failed!')