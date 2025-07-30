from fastapi import APIRouter, HTTPException
import tempfile
from api.utils.excel_utils import Orchestator
from api.utils.google_search import GoogleSearch

router = APIRouter()
orchestator = Orchestator()

@router.post("/search", status_code=200)
async def search(google_search: GoogleSearch) -> str:
    """Get Google search

    Args:
        google_search (GoogleSearch): Object including the string to search, country code and language to perform the search in

    Raises:
        HTTPException: Error 422 if anything goes wrong

    Returns:
        str: Stringified array of JSON object with search results
    """
    try:
        search_item = google_search.search
        language = google_search.language
        country_code = google_search.country_code
        commercial_activity = google_search.commercial_activity

        result = orchestator.search(search_item, language, country_code, commercial_activity)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/scraping", status_code=200)
async def scraping(google_search: GoogleSearch) -> GoogleSearch:
    """Extract web page content

    Args:
        google_search (GoogleSearch): Object containing URL to extract content from

    Raises:
        HTTPException: Error 422 if anything goes wrong

    Returns:
        GoogleSearch: Object that includes extracted content
    """
    try:
        result = orchestator.scraping(google_search)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.post("/read_pdf", status_code=200)
async def read_pdf(google_search: GoogleSearch) -> GoogleSearch:
    """Read PDF document

    Args:
        google_search (GoogleSearch): Object that includes URL of PDF to read

    Raises:
        HTTPException: Error 422 if anything goes wrong

    Returns:
        GoogleSearch: Object that includes content read from PDF
    """
    try:
        result = orchestator.read_pdf(google_search)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.post("/analyze", status_code=200)
async def analyze(google_search: GoogleSearch) -> GoogleSearch:
    """Perform AI analysis

    Args:
        google_search (GoogleSearch): Object that includes content to analyze

    Raises:
        HTTPException: Error 422 if anything goes wrong

    Returns:
        GoogleSearch: Object that includes parameters from interpretation results
    """
    try:
        temp_dir = tempfile.gettempdir()
        result = orchestator.analyze(google_search, temp_dir)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    

