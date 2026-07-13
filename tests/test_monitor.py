from src.monitor import extract_visible_text, generate_hash

html = """
<html>
    <head>
        <style>
            body { color: red; }
        </style>
        <script>
            console.log("hidden script");
        </script>
    </head>
    <body>
        <h1>Website Monitor</h1>
        <p>
            Page     content
            is visible.
        </p>
        <noscript>Hidden fallback text</noscript>
    </body>
</html>
"""

text = "Website content"
same_text = "Website content"
different_text = "Updated website content"

def test_extract_visible_text_removes_hidden_content():
    result = extract_visible_text(html)
    assert result == "Website Monitor Page content is visible."

def test_hash_generator():
    first_hash = generate_hash(text)
    same_hash = generate_hash(same_text)
    different_hash = generate_hash(different_text)
    assert first_hash == same_hash
    assert first_hash != different_hash
    assert len(first_hash) == 64