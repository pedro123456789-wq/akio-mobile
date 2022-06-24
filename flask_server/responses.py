from flask import make_response, jsonify, Response


def customResponse(success: bool, message: str = '', code: int = 404, **others) -> Response:
    """Wrapper for flask make_response function to make sending responses to front-end quicker

    Args:
        success (bool): Used to check if headers were valid and no errors were caught
        message (str, optional): Text to accompany response. Defaults to ''.
        code (int, optional): Status code of response. Defaults to 404.

    Returns:
        Response: Response object ready to be sent
    """
    
    newResponse = make_response(jsonify({
        "success": success,
        "message": message,
        **others
    }))

    newResponse.status_code = 200 if success else code
    return newResponse
