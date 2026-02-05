"""카카오 로그인 UI 템플릿. {auth_url}만 치환."""

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Eddi Robot Academy</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; }}
    .card {{ background: #fff; padding: 2rem; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center; max-width: 360px; width: 100%; }}
    h1 {{ margin: 0 0 0.5rem; font-size: 1.5rem; color: #333; }}
    .sub {{ color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; }}
    .btn {{ display: inline-block; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1rem; cursor: pointer; border: none; transition: opacity 0.2s; }}
    .btn-kakao {{ background: #FEE500; color: #191919; }}
    .btn-kakao:hover {{ opacity: 0.9; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Eddi Robot Academy</h1>
    <p class="sub">Eddi 로그인</p>
    <a href="{auth_url}" class="btn btn-kakao">카카오로 로그인</a>
  </div>
</body>
</html>
"""

ERROR_HTML = """<html><body><p>설정 오류: {msg}</p><p>.env에 KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI_HOST를 설정해주세요.</p></body></html>"""
