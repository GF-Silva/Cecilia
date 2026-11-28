from cecilia.extractors import FileMetadataExtractor, FileMetadata
import pytest

@pytest.mark.parametrize(
    'mime_type, type, filename',
    [
        ('audio/mpeg', 'mp3', 'file1'),
        ('audio/mpeg', 'mp3', 'file2'),
        ('audio/mpeg', 'mp3', 'file3'),
        ('audio/mpeg', 'mp3', 'file4'),
        ('video/webm', 'webm', 'file1'),
        ('video/webm', 'webm', 'file2'),
        ('video/webm', 'webm', 'file3'),
        ('image/jpeg', 'jpg', 'file1'),
        ('image/jpeg', 'jpg', 'file2'),
        ('image/jpeg', 'jpg', 'file3'),
        ('image/png', 'png', 'file1'),
        ('application/json', 'json', 'file1'),
        ('application/pdf', 'pdf', 'file1'),
        ('application/zip', 'zip', '42')
    ]
)
def test_success(file, mime_type, type, filename):
    gen_file = next(file(
        mime_type=mime_type,
        type=type,
        filename=filename
    ))

    file_metadata_extractor = FileMetadataExtractor()
    result = file_metadata_extractor(file=gen_file.stream)

    assert isinstance(result, FileMetadata)
    assert result.mime_type == mime_type