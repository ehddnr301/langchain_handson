from enum import Enum

MY_FOODS = {
    "한식": [
        "김치찌개",
        "된장찌개",
        "비빔밥",
        "불고기",
        "떡볶이",
        "김밥",
        "순두부찌개",
        "갈비탕",
        "순대국",
        "콩나물국밥",
    ],
    "중식": [
        "짜장면",
        "짬뽕",
        "탕수육",
        "양장피",
        "볶음밥",
        "마파두부",
        "깐풍기",
        "팔보채",
        "유산슬",
        "깐풍새우",
    ],
    "일식": [
        "초밥",
        "라멘",
        "우동",
        "돈까스",
        "규동",
        "카레",
        "오니기리",
        "오뎅",
        "타코야끼",
        "초밥",
    ],
    "패스트푸드": [
        "햄버거",
        "피자",
        "치킨",
        "샌드위치",
        "핫도그",
        "프렌치프라이",
        "치즈스틱",
        "피쉬앤칩스",
        "파스타",
        "스테이크",
    ],
    "분류불가": "분류불가",
}


class Foods(Enum):
    CHINESE_FOOD = "중식"
    JAPANESE_FOOD = "일식"
    FAST_FOOD = "패스트푸드"
    CANT_CLASSIFY = "분류불가"
    KOREAN_FOOD = "한식"
