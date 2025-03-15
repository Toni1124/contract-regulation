import re
from typing import Optional

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format."""
    if not isinstance(address, str):
        return False
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))

def validate_region(region: str) -> bool:
    """Validate if region is in allowed list."""
    allowed_regions = {'香港', '中国大陆', '不限', '澳门', '深圳'}
    return region in allowed_regions

def validate_operator(operator: str) -> bool:
    """Validate if operator is in allowed list."""
    allowed_operators = {'Admin', 'Operator'}
    return operator in allowed_operators

def validate_organization(org: str) -> bool:
    """Validate if organization is in allowed list."""
    allowed_orgs = {'中国人民银行', '中央网信办', '香港金管局'}
    return org in allowed_orgs 