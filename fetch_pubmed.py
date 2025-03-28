import requests

# PubMed API details
API_KEY = "your_api_key_here"  # Replace with your API key
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_articles(query="AI in Healthcare", max_results=10):
    """Fetches article IDs from PubMed based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
        "api_key": "98c9c704f0ce896e1981039086aa705dad08"
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "esearchresult" in data and "idlist" in data["esearchresult"]:
        article_ids = data["esearchresult"]["idlist"]
        return article_ids
    return []

def fetch_article_details(article_id):
    """Fetches full article details from PubMed."""
    params = {
        "db": "pubmed",
        "id": article_id,
        "retmode": "xml",
        "api_key": "98c9c704f0ce896e1981039086aa705dad08"
    }
    
    response = requests.get(DETAILS_URL, params=params)
    return response.text  # XML format

if __name__ == "__main__":
    articles = fetch_pubmed_articles()
    for article_id in articles:
        details = fetch_article_details(article_id)
        print(f"Article {article_id}: {details[:500]}...\n")  # Print first 500 chars
