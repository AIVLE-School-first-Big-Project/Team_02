from Alphabets import HEAD,TAIL,BODY,FIRST_KOREAN_UNICODE, NUMBERS



def Decompose(text):
    decom_list = []
    for ch in text:
        Uni_Value = ord(ch)
        if(48<=Uni_Value<=57): 
            decom_list.append((NUMBERS[Uni_Value-ord('0')]))
        if(Uni_Value==32) : 
            decom_list.append((' ',[[]]))
            continue
        if(Uni_Value==46) : 
            decom_list.append(('.',[[]]))
            continue
        Uni_Korean = Uni_Value - FIRST_KOREAN_UNICODE
        Uni_Head = Uni_Korean // (21 * 28)
        Uni_Body = Uni_Korean//28%21
        Uni_Tail = Uni_Korean % 28
        decom_list.append(HEAD[Uni_Head])
        decom_list.append(BODY[Uni_Body])
        decom_list.append(TAIL[Uni_Tail]) 
    return decom_list
Curr_Status =  0
HEAD_STATUS =  1
BODY_STATUS =  2
TAIL_STATUS =  3


def Compose(decom_list):
    Curr_Status = HEAD_STATUS
    
    for jamo in decom_list:
        letter = ''
        if(jamo == ' ') : 
            Curr_Status = HEAD_STATUS
            continue
        if(Curr_Status == HEAD_STATUS):
            pass
        if(Curr_Status == BODY_STATUS):
            pass
        if(Curr_Status == TAIL_STATUS):
            pass


if __name__ == "__main__":
    text = '한현수라고 합니다'
    text2 = '제가 직접 만든 패키지 입니다. 본 패캐지는 문장을 점자로 변환하는 과정의 일환으로 개발된 패키지입니다.'
    print(text)
    decom=Decompose(text)
    print(decom)
