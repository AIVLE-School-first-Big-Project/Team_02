from Alphabets import HEAD,TAIL,BODY,\
                      FIRST_KOREAN_UNICODE,LAST_KOREAN_UNICODE,\
                      NUM_BODY,NUM_TAIL,\
                      TAIL_DOUBLE,TAIL_SINGLE,\
                      NUMBERS


def is_jamo(Uni_Value:int) -> bool:
    """
    It verifies whether the input is Korean or not
    """
    if(FIRST_KOREAN_UNICODE<=Uni_Value<=LAST_KOREAN_UNICODE): return True
    return False
def get_Korean_Unicode(Uni_Value: int) -> int: 
    """
    returns substraction of unicode of current input character with first Korean unicode.
    """
    return Uni_Value - FIRST_KOREAN_UNICODE
def split_character(Uni_Korean: int)-> int: 
    """
    returns unicode of head, body and tail from the current input charcter 
    """    
    return Uni_Korean//(21 * 28), Uni_Korean//28%21, Uni_Korean % 28
def get_jamo_HEAD(Uni_Head: int) -> str: 
    """
    returns actual head of the current input character
    """
    return HEAD[Uni_Head]
def get_jamo_BODY(Uni_BODY: int) -> str: 
    """
    returns actual body of the current input character
    """
    return BODY[Uni_BODY]
def get_jamo_TAIL(Uni_TAIL: int) -> str: 
    """
    returns actual tail of the current input character
    """
    return TAIL[Uni_TAIL]
