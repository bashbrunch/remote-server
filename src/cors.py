from fastapi import Request, Response

async def cors_middleware(request: Request, call_next):
  origin = request.headers.get("origin")
  allowed = True

  if not allowed:
    return Response("CORS Failure", 401)

  response = Response(status_code=204)

  if request.method != "OPTIONS":
    try:
      response = await call_next(request)
    except Exception:
      response = Response(
        "Server refused the request",
        status_code=400
      )

  allowed_headers = ",".join(request.headers.keys() + [
    "authorization",
    "content-type",
  ])

  response.headers["Vary"] = "Origin"
  response.headers["Access-Control-Allow-Origin"] = origin or ""
  response.headers["Access-Control-Allow-Credentials"] = "true"
  response.headers["Access-Control-Allow-Methods"] = "*"
  response.headers["Access-Control-Allow-Headers"] = allowed_headers

  return response

