

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

Curr_Status =  0
HEAD_STATUS =  1
BODY_STATUS =  2
TAIL_STATUS =  3
TAIL2_STATUS = 4

def Compose(decom_list: list) -> str:
    """
    -DFA is on the README-
    when it gets list of jamo,
    return string of Korean text combining jamo.
    """
    Letter_Complete = False
    Curr_Status = HEAD_STATUS
    result_text = ''
    letter = ''

    for jamo in decom_list:
        if(jamo == ' ' or jamo=='.') :                   # ws finishes state 
            if(Curr_Status==3) : letter = Compose_letter(head,body)   # if curr_state is at tail, 
            elif(Curr_Status==4) : letter = Compose_letter(head,body, tail)
            result_text += letter+jamo
            Curr_Status = HEAD_STATUS
            letter = ''
            continue
    # state head
        if(Curr_Status == HEAD_STATUS):     
            print('HEAD STATE')
            if(jamo in HEAD): 
                Curr_Status=BODY_STATUS
                head = jamo
            else : 
                Curr_Status=HEAD_STATUS
                result_text += jamo
    # state body
        elif(Curr_Status == BODY_STATUS):   
            print('BODY STATE')
            if(jamo in BODY): 
                Curr_Status = TAIL_STATUS
                body = jamo
            else: 
                Curr_Status=HEAD_STATUS
                result_text += jamo
    # state tail
        elif(Curr_Status == TAIL_STATUS):   
            print('TAIL_STATE')
            if(jamo in TAIL_SINGLE) :
                tail = jamo
                Curr_Status = TAIL2_STATUS
            elif(jamo in TAIL_DOUBLE) : 
                Curr_Status = HEAD_STATUS
                tail = jamo
                letter = Compose_letter(head,body,tail)
                Letter_Complete = True
    # state to consider next jamo            
        elif(Curr_Status==TAIL2_STATUS):    
            print('TAIL2 STATE')
            if(jamo in HEAD):
                letter = Compose_letter(head,body,tail)
                Letter_Complete = True
                head = jamo
                Curr_Status = BODY_STATUS
            elif(jamo in BODY):
                letter = Compose_letter(head,body)
                Letter_Complete = True
                head = tail
                body = jamo
                Curr_Status = TAIL_STATUS
    # letter concat
        if(Letter_Complete):               
            print('Final State')
            result_text += letter
            Letter_Complete = False

    # last letter to compose
    if(Curr_Status==3) : return result_text+ Compose_letter(head,body)
    elif(Curr_Status==4) : return result_text + Compose_letter(head,body, tail)
    else : return result_text

def Compose_letter(head: str, body: str, tail:str ='') -> str:
    """
    When it gets either (head, body) or (head,body,tail) as a input, 
    Then it returns combined character based on the unicode 
    """
    return chr(FIRST_KOREAN_UNICODE+
              (HEAD.index(head))*NUM_BODY*NUM_TAIL+ 
              (BODY.index(body))*NUM_TAIL+ 
              (TAIL.index(tail))
              )


if __name__ == "__main__":
    from Alphabets import HEAD,TAIL,BODY,\
                      FIRST_KOREAN_UNICODE,LAST_KOREAN_UNICODE,\
                      NUM_BODY,NUM_TAIL,\
                      TAIL_DOUBLE,TAIL_SINGLE,\
                      NUMBERS


    text2 = '제가 직접 만든 패키지2 입니다. 본 패캐지는 문장을 점자로 변환하는 과정의 일환으로 개발된 패키지입니다.'
    print(text2)
    decom=Decompose(text2)
    print(decom)
    l = []
    for c in decom:
        if(c==''): continue
        l.append(c)
    print(l)
    text = Compose(l)
    print(text)
else:
    from .Alphabets import HEAD,TAIL,BODY,\
                      FIRST_KOREAN_UNICODE,LAST_KOREAN_UNICODE,\
                      NUM_BODY,NUM_TAIL,\
                      TAIL_DOUBLE,TAIL_SINGLE,\
                      NUMBERS