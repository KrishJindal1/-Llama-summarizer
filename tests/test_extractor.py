import io

from core.extractor import extract_txt

def test_extract_txt():

    file = io.BytesIO(
        b"Hello World"
    )

    result = extract_txt(file)

    assert result == "Hello World"