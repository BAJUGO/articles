from fastapi import Depends, Request, HTTPException

from .token_schema import AccessTokenData
from .token_enc_dec import get_token_from_cookies


def get_current_user_access_token(request: Request) -> AccessTokenData:
    try:
        token = get_token_from_cookies(request, token_type="access_token")
        return AccessTokenData(**token)
    except Exception as e:
        # Looooooooging
        raise HTTPException(status_code=401, detail=f"{e}")


def get_user_with_role(required_role: list[str]):
    def subfunction(
            user_token: AccessTokenData = Depends(get_current_user_access_token)
    ) -> AccessTokenData:
        if user_token.role not in required_role:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_token
    return subfunction


admin_dep = Depends(get_user_with_role(["admin"]))
admin_or_mod_dep = Depends(get_user_with_role(["admin", "moderator"]))