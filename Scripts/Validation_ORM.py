from Scripts.DTO import RisorsaDTOInsert,CommessaDTOInsert,AssenzaDTOInsert,LavoroDTOInsert
from sqlalchemy.orm import Session

def verify_session(session):
    if(not isinstance(session,Session)):
        raise(ValueError(f"La Sessione deve essere di tipo: Session"))
    if(not session.bind):
        raise (ValueError(f"La Sessione deve avere un DB Engine associato"))
    return session

def verify_risorsa(*args):
    for risorsa in args:
        if(not isinstance(risorsa,RisorsaDTOInsert) or not risorsa.email_utente or not risorsa.password_utente):
            raise ValueError("Il parametro passato non è di tipo Risorsa oppure è mancante di mail o password")
        
def verify_commessa(*args):
    for commessa in args:
        if(not isinstance(commessa,CommessaDTOInsert) or not commessa.nome_commessa):
            raise ValueError("Il parametro passato non è di tipo Commessa oppure è mancante di nome")

def verify_assenza(*args):
    for assenza in args:
        if(not isinstance(assenza,AssenzaDTOInsert) or not assenza.id_utente or not assenza.data_assenza or not assenza.durata_assenza or not assenza.tipo_assenza):
            raise ValueError("Il parametro passato non è di tipo Assenza oppure è mancante di un dato fondamentale")
        
def verify_lavoro(*args):
    for lavoro in args:
        if(not isinstance(lavoro,LavoroDTOInsert) or not lavoro.id_risorsa or not lavoro.id_commessa or not lavoro.data_lavoro or not lavoro.luogo_di_lavoro or not lavoro.ore_lavoro):
            raise ValueError("Il parametro passato non è di tipo Lavoro oppure è mancante di un dato fondamentale")