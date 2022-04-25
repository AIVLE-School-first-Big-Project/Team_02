from .Alphabets import HEAD,TAIL,BODY,FIRST_KOREAN_UNICODE, NUMBERS


def Decompose(text):
    sentence = []
    for ch in text:
        decom_list = []
        Uni_Value = ord(ch)
        print(ch, Uni_Value)
        if(48<=Uni_Value<=57): 
            decom_list.append((NUMBERS[Uni_Value-ord(0)]))
        if(Uni_Value==32) : 
            decom_list.append((' ',[[]]))
            continue
        if(Uni_Value==46) : 
            decom_list.append(('.',[[]]))
            continue
        Uni_Korean = Uni_Value - FIRST_KOREAN_UNICODE
        Uni_Head = Uni_Korean//(21*28)
        Uni_Body = Uni_Korean//28%21
        Uni_Tail = Uni_Korean%28
        decom_list.append(HEAD[Uni_Head][0])
        decom_list.append(BODY[Uni_Body][0])
        decom_list.append(TAIL[Uni_Tail][0])
        sentence.append(decom_list)
    return sentence

