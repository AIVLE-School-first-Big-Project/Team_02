


def Decompose(text: str) -> list:
    """
    When it gets Korean text, it seperates every character based on the unicode
    """
    decom_list = []
    for ch in text:
        Uni_Value = ord(ch)
        if(48<=Uni_Value<=57): 
            decom_list.append((NUMBERS[Uni_Value-ord('0')]))
        elif(Uni_Value==32) : decom_list.append(' ')
        elif(Uni_Value==32) : decom_list.append('\\n')
        elif(Uni_Value==46) : decom_list.append('.')
        elif(is_jamo(Uni_Value)):
            Uni_Korean = get_Korean_Unicode(Uni_Value)
            Uni_Head, Uni_Body, Uni_Tail = split_character(Uni_Korean)
            decom_list.append(get_jamo_HEAD(Uni_Head))
            decom_list.append(get_jamo_BODY(Uni_Body))
            decom_list.append(get_jamo_TAIL(Uni_Tail)) 
    return decom_list



if __name__ == "__main__":
    from utils import is_jamo,get_Korean_Unicode,split_character,get_jamo_HEAD,get_jamo_BODY,get_jamo_TAIL
    from Alphabets import NUMBERS

    text2 = '본 패캐지는 문장을 점자로 변환하는 과정의 일환으로 개발된 패키지입니다.'
    print(text2)
    decom=Decompose(text2)
    print(decom)
else:
    from .Alphabets import NUMBERS
    from .utils import is_jamo,get_Korean_Unicode,split_character,get_jamo_HEAD,get_jamo_BODY,get_jamo_TAIL