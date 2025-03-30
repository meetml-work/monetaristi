from bs4 import BeautifulSoup


def clean_word_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove all inline styles (font-size, color, etc.)
    for tag in soup.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]

    # Remove Word-specific tags like <o:p>
    for o_tag in soup.find_all("o:p"):
        o_tag.unwrap()

    # Remove unnecessary <span> tags
    for span in soup.find_all("span"):
        if not span.attrs:
            span.unwrap()

    return str(soup)