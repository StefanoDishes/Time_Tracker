from email_validator import validate_email, EmailNotValidError

def verify_str(*args)->bool:
    for s in args:
        if(s is not None and not isinstance(s,str)):
            raise ValueError("Non sono state passate delle stringhe")
    return True

def verify_int(*args)->bool:
    for s in args:
        if(s is not None and not isinstance(s,int)):
            raise ValueError("Non sono state passati degli int")
    return True

def verify_float(*args)->bool:
    for s in args:
        if(s is not None and not isinstance(s,float)):
            raise ValueError("Non sono state passati degli int")
    return True

def verify_mail(mail:str) -> bool :
        try:
            verify_str(mail)
            try:
                validate_email(mail)
                return True
            except EmailNotValidError as e:
                print(f"L'indirizzo email non è valido: {e}")
                return False
        except ValueError as ve:
            print(f"La mail {mail} non è una stringa: {ve}")
            return False