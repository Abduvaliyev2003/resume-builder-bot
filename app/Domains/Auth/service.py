from app.Shared.api_client import api

class AuthService:

    async def login(self, email, password):
        return await api.post("/login",{
            "email": email,
            "password": password
        })

    def register(self,name:str, email, password):
        return await api.post("/register",{
            "name": name,
            "email": email,
            "password": password
        })
    async def logout(self, token):
        return await api.post("/logout", headers={
            "Authorization": f"Bearer {token}"
        })


auth_service = AuthService()