instructions = [
    'DROP TABLE IF EXISTS email;',
    """
            CREATE TABLE email (
                id SERIAL PRIMARY KEY ,
                email VARCHAR NOT NULL,
                subject VARCHAR NOT NULL,
                content VARCHAR NOT NULL
            )
        """
]
