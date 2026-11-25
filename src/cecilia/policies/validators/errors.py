from cecilia.core.exceptions import BaseError

class FileTooBigError(BaseError):
    def __init__(
        self,
        size: int,
        max_size: int,
        resource: str,
        title: str = 'File too big',
        status_code: int = 413,
        error_code: str = 'FILE_TOO_BIG'
    ):
        super().__init__(
            title=title,
            status_code=status_code,
            message=f'The file size of {size} is more than the limit allowed for {resource}',
            error_code=error_code,
            values={
                "size": size,
                "max_size": max_size
            }
        )
