FIRST_KOREAN_UNICODE = 0xAC00
LAST_KOREAN_UNICODE = 0xD7A3

NUM_HEAD = 19
HEAD_DOUBLE_CONSONANT = [1, 4, 8, 10, 13]
HEAD = [
    u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
    ]

NUM_BODY = 21
BODY = [
    u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ',
    u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ',
    u'ㅣ'
    ]

NUM_TAIL = 28
TAIL_DOUBLE_CONSONANT = [2, 3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 18, 20]
TAIL = [
    u'', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ',
    u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
]
TAIL_SINGLE = [
    u'', u'ㄱ', u'ㄴ', u'ㄷ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅅ', u'ㅇ', u'ㅈ',
    u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
]
TAIL_DOUBLE = [
    u'ㄲ', u'ㄳ', u'ㄵ', u'ㄶ', u'ㄺ', u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ',
    u'ㅀ', u'ㅄ', u'ㅆ'
]

NUMBERS = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
]
ENGLISH_ALPHABETS = {
    'a': [[1, 0, 0, 0, 0, 0]],
    'b': [[1, 1, 0, 0, 0, 0]],
    'c': [[1, 0, 0, 1, 0, 0]],
    'd': [[1, 0, 0, 1, 1, 0]],
    'e': [[1, 0, 0, 0, 1, 0]],
    'f': [[1, 1, 0, 1, 0, 0]],
    'g': [[1, 1, 0, 1, 1, 0]],
    'h': [[1, 1, 0, 0, 1, 0]],
    'i': [[0, 1, 0, 1, 0, 0]],
    'j': [[0, 1, 0, 1, 1, 0]],
    'k': [[1, 0, 1, 0, 0, 0]],
    'l': [[1, 1, 1, 0, 0, 0]],
    'm': [[1, 0, 1, 1, 0, 0]],
    'n': [[1, 0, 1, 1, 1, 0]],
    'o': [[1, 0, 1, 0, 1, 0]],
    'p': [[1, 1, 1, 1, 0, 0]],
    'q': [[1, 1, 1, 1, 1, 0]],
    'r': [[1, 1, 1, 0, 1, 0]],
    's': [[0, 1, 1, 1, 0, 0]],
    't': [[0, 1, 1, 1, 1, 0]],
    'u': [[1, 0, 1, 0, 0, 1]],
    'v': [[1, 1, 1, 0, 0, 1]],
    'w': [[0, 1, 1, 1, 1, 1]],
    'x': [[1, 0, 1, 1, 0, 1]],
    'y': [[1, 0, 1, 1, 1, 1]],
    'z': [[1, 0, 1, 0, 1, 1]],

    'A': [[0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0]],
    'B': [[0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0]],
    'C': [[0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0]],
    'D': [[0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 0]],
    'E': [[0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0]],
    'F': [[0, 0, 0, 0, 0, 1], [1, 1, 0, 1, 0, 0]],
    'G': [[0, 0, 0, 0, 0, 1], [1, 1, 0, 1, 1, 0]],
    'H': [[0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0]],
    'I': [[0, 0, 0, 0, 0, 1], [0, 1, 0, 1, 0, 0]],
    'J': [[0, 0, 0, 0, 0, 1], [0, 1, 0, 1, 1, 0]],
    'K': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0]],
    'L': [[0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0]],
    'M': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0]],
    'N': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0]],
    'O': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0]],
    'P': [[0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 0, 0]],
    'Q': [[0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 0]],
    'R': [[0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 0]],
    'S': [[0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 0, 0]],
    'T': [[0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 0]],
    'U': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 1]],
    'V': [[0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 1]],
    'W': [[0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1]],
    'X': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 1]],
    'Y': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 1]],
    'Z': [[0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 1]],


    ',': [[0, 1, 0, 0, 0, 0]],
    '.': [[0, 1, 0, 0, 1, 1]],
    '-': [[0, 1, 0, 0, 1, 0]],
    '?': [[0, 1, 1, 0, 0, 1]],
    '_': [[0, 0, 1, 0, 0, 1]],
    '!': [[0, 1, 1, 0, 1, 0]],
}
