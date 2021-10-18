class Stats:

    @classmethod
    def from_boto(cls, s3: dict) -> dict:
        return dict(
            size=s3.get('ContentLength'),
            last_modified=s3.get('LastModified'),
            content_type=s3.get('ContentType'),
            Etag=s3.get('Etag')
        )