import re
from validate_docbr import CPF


class CPFValidator:
    @staticmethod
    def clean_cpf(cpf: str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', cpf)

    @staticmethod
    def validate(cpf: str) -> tuple[bool, str]:
        cpf = CPFValidator.clean_cpf(cpf)

        cpf_validator = CPF()
        is_valid = cpf_validator.validate(cpf)
        return is_valid, cpf
