from bs4 import BeautifulSoup
import hashlib

def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    
    text = soup.get_text(" ")
    cleaned_text = " ".join(text.split())

    return cleaned_text

def generate_hash(text):

    encoded_text = text.encode("utf-8")
    h = hashlib.new("sha256")
    h.update(encoded_text)
    return h.hexdigest()