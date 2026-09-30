from pathlib import Path

import pytest

from core.document_loader import extract_document_text


@pytest.mark.skipif(__import__('importlib').util.find_spec('fitz') is None, reason='PyMuPDF is not installed')
def test_pdf_extraction_extracts_text(tmp_path):
    import fitz

    file_path = tmp_path / 'demo.pdf'
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), 'This is a sample PDF for workshop testing.')
    doc.save(file_path)
    doc.close()

    result = extract_document_text(file_path)
    assert result['file_type'] == 'pdf'
    assert 'sample PDF' in result['text']
    assert result['page_count'] >= 1


def test_docx_extraction_extracts_text(tmp_path):
    from docx import Document

    file_path = tmp_path / 'demo.docx'
    document = Document()
    document.add_paragraph('This is a sample DOCX paragraph for workshop testing.')
    document.save(file_path)

    result = extract_document_text(file_path)
    assert result['file_type'] == 'docx'
    assert 'sample DOCX' in result['text']
    assert result['page_count'] == 1
