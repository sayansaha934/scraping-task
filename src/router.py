from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from .request import ScrapperRequest
from db import SESSION
from src.services.scraper import ScraperService
from src.auth import authenticate
from src.services.notification import NotificationService
router = APIRouter()


@router.post("")
def scrap(args: ScrapperRequest, _=Depends(authenticate)):
    try:
        total_products = ScraperService().scrape_page(
            SESSION=SESSION, page_limit=args.page, search_string=args.search_string
        )
        message = f"Total products scrapped and updated in DB: {total_products}"
        NotificationService().send_notification(message)
        print(message)
        SESSION.close()
        return JSONResponse(status_code=200, content={"message": message})
    except Exception as e:
        print(e)
        SESSION.rollback()
        return JSONResponse(status_code=500, content=str(e))
