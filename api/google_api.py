import os
from googleapiclient.discovery import build

def search_internet(query):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        cse_id = os.getenv("GOOGLE_CSE_ID")
        if not api_key or not cse_id:
            return "API Key ou ID do mecanismo de pesquisa não configurados."
        
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id).execute()
        results = res.get('items', [])
        
        search_results = []
        for item in results[:5]:
            search_results.append(f"{item['title']}: {item['snippet']}")
        
        return "\n".join(search_results)
    except Exception as e:
        return f"Erro ao realizar a pesquisa: {e}"