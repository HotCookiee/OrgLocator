from fastapi import Response,Request



def get_token_form_cookie_by_name(name: str , request: Request):
    token = request.cookies.get(name)
    return token
    