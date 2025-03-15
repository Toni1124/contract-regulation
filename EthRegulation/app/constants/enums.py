from enum import Enum

class ListType(Enum):
    WHITE = 1
    BLACK = 2

class Region(Enum):
    HONG_KONG = '香港'
    MAINLAND = '中国大陆'
    UNLIMITED = '不限'
    MACAU = '澳门'
    SHENZHEN = '深圳'

class Operator(Enum):
    ADMIN = 'Admin'
    OPERATOR = 'Operator'

class Organization(Enum):
    PBOC = '中国人民银行'
    CAC = '中央网信办'
    HKMA = '香港金管局' 