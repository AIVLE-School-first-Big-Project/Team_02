from .Alphabets import HEAD,TAIL,BODY,FIRST_KOREAN_UNICODE, NUMBERS


def Decompose(text):
    decom_list = []
    for ch in text:
        Uni_Value = ord(ch)
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
        decom_list.append(HEAD[Uni_Head])
        decom_list.append(BODY[Uni_Body])
        decom_list.append(TAIL[Uni_Tail]) 
    return decom_list

