import httpx
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
from urllib.parse import urlencode
from app.core.config import settings
from app.database.constants import ResponseMessage

class SocialSignUp():
    
    async def google_signup(self):
        try:
            params = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "response_type": "code",
                "prompt": "consent",
                "scope": "openid email profile",
                "access_type": "offline",
                "state": ""
            }
            return f"{settings.GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"
        
        except Exception as e:
            raise e
    
    async def google_login(self):
        try:
            params = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "response_type":"code",
                "scope": "openid email profile",
                "access_type": "offline"
            }
            return f"{settings.GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"
        
        except Exception as e:
            raise e
    
    async def google_callback(self, request):
        try:
            code = request.query_params.get("code")
            
            client_id = settings.GOOGLE_CLIENT_ID
            client_secret = settings.GOOGLE_CLIENT_SECRET
            token_endpoint = settings.GOOGLE_TOKEN_ENDPOINT
            user_endpoint = settings.GOOGLE_USER_ENDPOINT
            redirect_uri = settings.GOOGLE_REDIRECT_URI
            
            details = await self.id_token_social_provider_endpoint(
                code, 
                client_id, 
                client_secret,
                token_endpoint,
                user_endpoint,
                redirect_uri
            )
            
            print(details)
            
        except Exception as e:
            raise e
        
    async def user_social_provider_endpoint(self, code, client_id, client_secret, token_endpoint, user_endpoint, redirect_uri):
        try:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
                "grant_type": "authorization_code"
            }
            
            async with httpx.AsyncClient() as client:
                token_response = await client.post(token_endpoint, data= data)
                token_data = token_response.json()
                access_token = token_data.get("access_token")
                
                headers = {"Authorization": f"Bearer {access_token}"}
                user_response = await client.get(user_endpoint, headers= headers)
                user_details = user_response.json()
                
                return user_details
            
        except Exception as e:
            raise e
        
    async def id_token_social_provider_endpoint(self, code, client_id, client_secret, token_endpoint, user_endpoint, redirect_uri):
        try:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
                "grant_type": "authorization_code"
            }
            
            async with httpx.AsyncClient() as client:
                token_response = await client.post(token_endpoint, data= data)
                token_data = token_response.json()
                
                if "id_token" not in token_data:
                    raise HTTPException(
                        status_code=400,
                        detail=ResponseMessage.GOOGLE_TOKEN_EXCHANGE_FAILED
                    )
                
            id_info = id_token.verify_oauth2_token(
                token_data['id_token'],
                requests.Request(),
                client_id
            )
            
            if not id_info.get("email_verified", False):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ResponseMessage.GOOGLE_EMAIL_NOT_VERIFIED
                )
            
            return {
                "email": id_info['email'],
                "name": id_info.get("name", "Unknown"),
                "google_id": id_info['sub']
            }
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e