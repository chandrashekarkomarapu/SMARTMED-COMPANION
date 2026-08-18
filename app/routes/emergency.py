from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["emergency"])


@router.get("/emergency")
async def emergency_page(request: Request):
    try:
        template = request.app.state.templates.env.get_template("emergency.html")
        html_content = template.render(request=request)
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading emergency page: {str(e)}</h1>", status_code=500)
