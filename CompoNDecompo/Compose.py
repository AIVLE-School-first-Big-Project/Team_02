Curr_Status = 0
HEAD_STATUS = 1
BODY_STATUS = 2
TAIL_STATUS = 3
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
        if(jamo == ' ' or jamo == '.'):  # ws finishes state
            if(Curr_Status == 3):
                letter = Compose_letter(head, body)
            # if curr_state is at tail,
            elif(Curr_Status == 4):
                letter = Compose_letter(head, body, tail)
            result_text += letter + jamo
            Curr_Status = HEAD_STATUS
            letter = ''
            continue
    # state head
        if(Curr_Status == HEAD_STATUS):
            print('HEAD STATE')
            if(jamo in HEAD):
                Curr_Status = BODY_STATUS
                head = jamo
            else:
                Curr_Status = HEAD_STATUS
                result_text += jamo
    # state body
        elif(Curr_Status == BODY_STATUS):
            print('BODY STATE')
            if(jamo in BODY):
                Curr_Status = TAIL_STATUS
                body = jamo
            else:
                Curr_Status = HEAD_STATUS
                result_text += jamo
    # state tail
        elif(Curr_Status == TAIL_STATUS):
            print('TAIL_STATE')
            if(jamo in TAIL_SINGLE):
                tail = jamo
                Curr_Status = TAIL2_STATUS
            elif(jamo in TAIL_DOUBLE):
                Curr_Status = HEAD_STATUS
                tail = jamo
                letter = Compose_letter(head, body, tail)
                Letter_Complete = True
    # state to consider next jamo
        elif(Curr_Status == TAIL2_STATUS):
            print('TAIL2 STATE')
            if(jamo in HEAD):
                letter = Compose_letter(head, body, tail)
                Letter_Complete = True
                head = jamo
                Curr_Status = BODY_STATUS
            elif(jamo in BODY):
                letter = Compose_letter(head, body)
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
    if(Curr_Status == 3):
        return result_text + Compose_letter(head, body)
    elif(Curr_Status == 4):
        return result_text + Compose_letter(head, body, tail)
    else:
        return result_text


def Compose_letter(head: str, body: str, tail: str = '') -> str:
    """
    When it gets either (head, body) or (head,body,tail) as a input,
    Then it returns combined character based on the unicode
    """
    return chr(FIRST_KOREAN_UNICODE +
               (HEAD.index(head))*NUM_BODY*NUM_TAIL +
               (BODY.index(body))*NUM_TAIL +
               (TAIL.index(tail))
               )


if __name__ == "__main__":
    from Alphabets import HEAD, TAIL, BODY,\
                            FIRST_KOREAN_UNICODE,\
                            NUM_BODY, NUM_TAIL,\
                            TAIL_DOUBLE, TAIL_SINGLE
    decom = ['ㅈ', 'ㅔ', '', 'ㄱ', 'ㅏ', '', ' ', 'ㅈ', 'ㅣ',
             'ㄱ', 'ㅈ', 'ㅓ', 'ㅂ', ' ', 'ㅁ', 'ㅏ', 'ㄴ',
             'ㄷ', 'ㅡ', 'ㄴ', ' ', 'ㅍ', 'ㅐ', '', 'ㅋ', 'ㅣ',
             '', 'ㅈ', 'ㅣ', '', '2', ' ', 'ㅇ', 'ㅣ', 'ㅂ',
             'ㄴ', 'ㅣ', '', 'ㄷ', 'ㅏ', '', '.', ' ', 'ㅂ',
             'ㅗ', ' ㄴ', ' ', 'ㅍ', 'ㅐ', '', 'ㅋ', 'ㅐ', '',
             'ㅈ', 'ㅣ', '', 'ㄴ', 'ㅡ', 'ㄴ', ' ', 'ㅁ', 'ㅜ',
             'ㄴ', 'ㅈ', 'ㅏ', 'ㅇ', 'ㅇ', 'ㅡ', 'ㄹ', ' ', 'ㅈ',
             'ㅓ', 'ㅁ', 'ㅈ', 'ㅏ', '', 'ㄹ', 'ㅗ', '', ' ',
             'ㅂ', 'ㅕ', 'ㄴ', 'ㅎ', 'ㅘ', 'ㄴ', 'ㅎ', 'ㅏ', '',
             'ㄴ', 'ㅡ', 'ㄴ', ' ', 'ㄱ', 'ㅘ', '', 'ㅈ', 'ㅓ',
             'ㅇ', 'ㅇ', 'ㅢ', '', ' ', 'ㅇ', 'ㅣ', 'ㄹ', 'ㅎ',
             'ㅘ', 'ㄴ', 'ㅇ', 'ㅡ', '', 'ㄹ', 'ㅗ', '', ' ', 'ㄱ',
             'ㅐ', '', 'ㅂ', 'ㅏ', 'ㄹ', 'ㄷ', 'ㅚ', 'ㄴ', ' ', 'ㅍ',
             'ㅐ', '', 'ㅋ', 'ㅣ', '', 'ㅈ', 'ㅣ', '', 'ㅇ', 'ㅣ',
             'ㅂ', 'ㄴ', 'ㅣ', '', 'ㄷ', 'ㅏ', '', '.']
    l = []
    for c in decom:
        if(c == ''):
            continue
        l.append(c)
    print(l)
    text = Compose(l)
    print(text)
else:
    from .Alphabets import HEAD, TAIL, BODY,\
                      FIRST_KOREAN_UNICODE,\
                      NUM_BODY, NUM_TAIL,\
                      TAIL_DOUBLE, TAIL_SINGLE
