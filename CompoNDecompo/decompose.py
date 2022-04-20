import Alphabets


def Decompose(text):
    decom_list = []
    for t in text:
        if(ord(t)==32) : 
            decom_list.append('')
            continue
        one = ord(t) - Alphabets.FIRST_KOREAN_UNICODE
        decom_list.append(Alphabets.HEAD[one//(21*28)])
        decom_list.append(Alphabets.BODY[one//28%21])
        decom_list.append(Alphabets.TAIL[one%28]) 
    return decom_list

