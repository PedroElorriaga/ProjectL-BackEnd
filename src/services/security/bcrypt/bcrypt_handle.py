import bcrypt


class BcryptHandle:

    @staticmethod
    def hash_content(input: str) -> bytes:
        hashed_input = bcrypt.hashpw(input.encode('utf-8'), bcrypt.gensalt())
        return hashed_input

    @staticmethod
    def check_content(input: str, stored_hash: bytes) -> bool:
        return bcrypt.checkpw(input.encode('utf-8'), stored_hash.encode('utf-8'))
