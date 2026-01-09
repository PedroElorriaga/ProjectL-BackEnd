import bcrypt


class BcryptHandle:

    @staticmethod
    def hash_content(input: str) -> str:
        hashed_input = bcrypt.hashpw(input.encode('utf-8'), bcrypt.gensalt())
        return hashed_input.decode('utf-8')

    @staticmethod
    def check_content(input: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(input.encode('utf-8'), stored_hash.encode('utf-8'))
