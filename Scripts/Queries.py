from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy import select,desc
from Scripts.Entities import Risorsa,Commessa,Lavoro,Assenza
from Scripts.Validation_Data import verify_str,verify_int,verify_float
from Scripts.Validation_ORM import verify_risorsa,verify_session,verify_commessa,verify_lavoro,verify_assenza
from Scripts.DTO import RisorsaDTORead,RisorsaDTOInsert,CommessaDTORead,CommessaDTOInsert,LavoroDTOInsert,AssenzaDTOInsert,LavoroDTORead,AssenzaDTORead

def loginRisorsa(email:str,password:str,session)->RisorsaDTORead|None:
    """Restituisce la risorsa da DB come DTO, None se non trova nessun utente con quella mail e password"""
    #Controlli su input funzione
    verify_str(email,password)
    session = verify_session(session)
    
    #Query
    result=session.scalar(select(Risorsa).where(Risorsa.email_utente==email,Risorsa.password_utente==password))
    if(result):
        return RisorsaDTORead.risorsa_to_DTO(result)
    else:
        return None

def findRisorsaByMail(email:str,session:Session)->RisorsaDTORead:
    """Restituisce la risorsa da DB come DTO, None se non trova nessun utente con quella mail"""
    #Controlli su input funzione
    verify_str(email)
    session=verify_session(session)
    
    #Query
    result=session.scalar(select(Risorsa).where(Risorsa.email_utente==email))
    if(result):
        return RisorsaDTORead.risorsa_to_DTO(result)
    else:
        return None

def findRisorsaById(id:int,session:Session)->RisorsaDTORead|None:
    verify_int(id)
    session=verify_session(session)

    result=session.scalar(select(Risorsa).where(Risorsa.id==id))
    if(result):
        return RisorsaDTORead.risorsa_to_DTO(result)
    else:
        return None

def findCommessaByName(nome_commessa:str,session:Session)->CommessaDTORead|None:
    """Restituisce la commessa da DB come DTO, None se non trova nessuna commessa con quel nome"""
    #Controlli su input funzione
    verify_str(nome_commessa)
    session=verify_session(session)

    #Query
    result=session.scalar(select(Commessa).where(Commessa.nome_commessa==nome_commessa))

    if(result):
        return CommessaDTORead.commessa_to_DTO(result)
    else:
        return None

def findLavoroByData(id_risorsa:int,id_commessa:int,data:str,durata:float,luogo:str,session:Session)->LavoroDTORead|None:
    """Restituisce il lavoro da DB come DTO, None se non trova nessun lavoro con gli stessi dati"""
    #Controlli su input funzione
    verify_str(data,luogo)
    verify_int(id_risorsa,id_commessa)
    verify_float(durata)
    verify_session(session)

    #Query
    result=session.scalar(select(Lavoro).where(Lavoro.id_risorsa==id_risorsa,Lavoro.id_commessa==id_commessa,Lavoro.data_lavoro==data,Lavoro.ore_lavoro==durata,Lavoro.luogo_di_lavoro==luogo))

    if(result):
        return LavoroDTORead.lavoro_to_DTO(result)
    else:
        return None

def findAllCommesseDict(session:Session):
    verify_session(session)

    query_results=session.scalars(select(Commessa).order_by(Commessa.nome_commessa)).all()
    if query_results:
        results={}
        for result in query_results:
            results.update({result.id:result.nome_commessa})
        return results
    else:
        return None

def findLavoriByRisorsa(id_risorsa:int,session:Session):
    verify_int(id_risorsa)
    verify_session(session)

    query_results= session.scalars(select(Lavoro).where(Lavoro.id_risorsa==id_risorsa).order_by(Lavoro.data_lavoro.desc())).all()
    commesse=findAllCommesseDict(session)
    if query_results and commesse:
        results=[]
        for result in query_results:
            results.append({'Id':result.id,'Commessa':commesse[result.id_commessa],'ore':result.ore_lavoro,'data':result.data_lavoro,'luogo':result.luogo_di_lavoro,'note':result.descrizione_lavoro})
        return results
    else:
        return None

def findAllCommesse(session:Session):
    verify_session(session)

    query_results=session.scalars(select(Commessa).order_by(Commessa.nome_commessa)).all()
    if query_results:
        results={}
        for result in query_results:
            results.update({result.nome_commessa:result.id})
        return results
    else:
        return None

def findAllCommesseAdmin(session:Session):
    verify_session(session)
    query_results=session.scalars(select(Commessa).order_by(Commessa.nome_commessa)).all()
    if query_results:
        commesse=[]
        for commessa in query_results:
            commesse.append({'Id':commessa.id,'Nome':commessa.nome_commessa,'Stato':commessa.stato_commessa,'Inizio':commessa.inizio_commessa,'Fine':commessa.fine_commessa,'Note':commessa.note_commessa})
        return commesse
    else:
        return None

def findAllRisorseAdmin(session:Session):
    verify_session(session)
    stato={
        1:'attiva',
        0:'disattiva'
    }
    query_results=session.scalars(select(Risorsa).order_by(Risorsa.cognome_utente)).all()
    if query_results:
        risorse=[]
        for risorsa in query_results:
            risorse.append({'Id':risorsa.id,'Nome':risorsa.nome_utente,'Cognome':risorsa.cognome_utente,'Email':risorsa.email_utente,'Tipo':risorsa.tipo_utente,'Stato':stato[risorsa.stato_utente]})
        return risorse
    else:
        return None
            
def findAllActiveCommesse(session:Session):
    verify_session(session)

    query_results=session.scalars(select(Commessa).where(Commessa.stato_commessa=='aperta').order_by(Commessa.nome_commessa)).all()
    if query_results:
        results={}
        for result in query_results:
            results.update({result.nome_commessa:result.id})
        return results
    else:
        return None

def findAssenzaByData(id_utente:int,tipo_assenza:str,durata_assenza:int,data_assenza:str,note_assenza:str,session:Session)->AssenzaDTORead|None:
    """Restituisce l'assenza da DB come DTO, None se non trova nessuna assenza con gli stessi dati"""
    #Controlli su input funzione
    verify_str(tipo_assenza,data_assenza,note_assenza)
    verify_int(id_utente,durata_assenza)
    verify_session(session)

    #Query
    result=session.scalar(select(Assenza).where(Assenza.id_utente==id_utente,Assenza.tipo_assenza==tipo_assenza,Assenza.durata_assenza==durata_assenza,Assenza.data_assenza==data_assenza,Assenza.note_assenza==note_assenza))

    if(result):
        return AssenzaDTORead.assenza_to_DTO(result)
    else:
        return None

def findAssenzeByRisorsa(id_risorsa:int,session:Session):
    verify_int(id_risorsa)
    verify_session(session)

    query_results= session.scalars(select(Assenza).where(Assenza.id_utente==id_risorsa).order_by(Assenza.data_assenza.desc())).all()
    if query_results:
        results=[]
        for result in query_results:
            results.append({'Id':result.id,'tipo':result.tipo_assenza,'durata':result.durata_assenza,'data':result.data_assenza,'note':result.note_assenza})
        return results
    else:
        return None

def insertRisorsa(risorsaDTO:RisorsaDTOInsert,session:Session)->Risorsa|None:
    """Restituisce la risorsa inserita, eccezione se esiste già un utente con la stessa email o non è stato possibile mappare il DTO"""
    #Controlli su input funzione
    verify_risorsa(risorsaDTO)
    session=verify_session(session)

    #Controllo su risorse uguali
    if(findRisorsaByMail(risorsaDTO.email_utente,session)):
        return Exception("La risorsa è già presente nel db") 
    
    #Query
    risorsa = risorsaDTO.DTO_to_risorsa()
    if(risorsa):
        session.add(risorsa)
        session.commit()
        return risorsa
    else:
        raise Exception("Non è stato possibile mappare il DTO risorsa poichè non ha passato la validazione")

def insertCommessa(commessaDTO:CommessaDTOInsert,session:Session):
    """Restituisce la commessa inserita, eccezione se esiste già una commessa con lo stesso nome o non è stato possibile mappare il DTO"""
    #Controlli su input funzione
    verify_commessa(commessaDTO)
    session=verify_session(session)

    #Controllo su commesse uguali
    if(findCommessaByName(commessaDTO.nome_commessa,session)):
        raise Exception("La commessa è gia presente nel DB")

    #Query
    commessa=commessaDTO.DTO_to_commessa()
    if(commessa):
        session.add(commessa)
        session.commit()
        return commessa
    else:
        raise Exception("Non è stato possibile mappare il DTO commessa poichè non ha passato la validazione")

def insertCommesse(commesse:List,session:Session):
    pass

def insertLavoro(lavoroDTO:LavoroDTOInsert,session:Session):
    #Controlli su input funzione
    verify_lavoro(lavoroDTO)
    session=verify_session(session)

    #Controllo su lavori uguali
    if(findLavoroByData(id_risorsa=lavoroDTO.id_risorsa,id_commessa=lavoroDTO.id_commessa,data=lavoroDTO.data_lavoro,durata=lavoroDTO.ore_lavoro,luogo=lavoroDTO.luogo_di_lavoro,session=session)):
        raise Exception("Il lavoro è gia presente nel DB")

    #Query
    lavoro=lavoroDTO.DTO_to_lavoro()
    if(lavoro):
        session.add(lavoro)
        session.commit()
        return lavoro
    else:
        raise Exception("Non è stato possibile mappare il DTO lavoro poichè non ha passato la validazione")

def insertLavori(lavori:List[Lavoro],session:Session):
    pass

def insertAssenza(assenzaDTO:AssenzaDTOInsert,session:Session):
    #Controlli su input funzione
    verify_assenza(assenzaDTO)
    session=verify_session(session)

    #Controllo su lavori uguali
    if(findAssenzaByData(id_utente=assenzaDTO.id_utente,tipo_assenza=assenzaDTO.tipo_assenza,durata_assenza=assenzaDTO.durata_assenza,data_assenza=assenzaDTO.data_assenza,note_assenza=assenzaDTO.note_assenza,session=session)):
        raise Exception("L'assenza è gia presente nel DB")

    #Query
    assenza=assenzaDTO.DTO_to_assenza()
    if(assenza):
        session.add(assenza)
        session.commit()
        return assenza
    else:
        raise Exception("Non è stato possibile mappare il DTO assenza poichè non ha passato la validazione")

def insertAssenze(assenze:List[Assenza],session:Session):
    pass

def updatePasswordRisorsa(risorsaDTO:RisorsaDTOInsert,session:Session)->RisorsaDTORead|None:
    """Aggiorna la password della risorsa che trova nel db"""
    #Controllo su input funzione
    verify_risorsa(risorsaDTO)
    verify_session(session)
    
    risorsa_update = session.scalar(select(Risorsa).where(Risorsa.email_utente==risorsaDTO.email_utente,Risorsa.nome_utente==risorsaDTO.nome_utente,Risorsa.cognome_utente==risorsaDTO.cognome_utente))
    if(risorsa_update):
        risorsa_update.password_utente=risorsaDTO.password_utente
        session.commit()
        return RisorsaDTORead.risorsa_to_DTO(risorsa_update)
    else:
        return None

def resetPassword(id:int,password:str,session:Session)->RisorsaDTORead|None:
    verify_int(id)
    verify_str(password)
    verify_session(session)

    risorsa_update=session.scalar(select(Risorsa).where(Risorsa.id==id))
    if(risorsa_update):
        risorsa_update.password_utente=password
        session.commit()
        return RisorsaDTORead.risorsa_to_DTO(risorsa_update)
    else:
        return None

def updateRisorsa(id:int,nome:str,cognome:str,session:Session)->RisorsaDTORead|None:
    """Aggiorna la risorsa che trova nel db"""
    #Controllo su input funzione
    verify_str(nome,cognome)
    verify_int(id)
    verify_session(session)

    risorsa_update=session.scalar(select(Risorsa).where(Risorsa.id==id))
    if(risorsa_update):
        risorsa_update.nome_utente=nome
        risorsa_update.cognome_utente=cognome
        session.commit()
        return RisorsaDTORead.risorsa_to_DTO(risorsa_update)
    else:
        return None

def updateRisorsaAdmin(id:int,nome:str,cognome:str,mail:str,tipo:str,stato:int,session:Session)->RisorsaDTORead|None:
    """Aggiorna la risorsa che trova nel db"""
    #Controllo su input funzione
    verify_str(nome,cognome,mail,tipo)
    verify_int(id,stato)
    verify_session(session)

    risorsa_update=session.scalar(select(Risorsa).where(Risorsa.id==id))
    if(risorsa_update):
        risorsa_update.nome_utente=nome
        risorsa_update.cognome_utente=cognome
        risorsa_update.email_utente=mail
        risorsa_update.tipo_utente=tipo
        risorsa_update.stato_utente=stato
        session.commit()
        return RisorsaDTORead.risorsa_to_DTO(risorsa_update)
    else:
        return None

def updateLavoro(id:int,lavoroDTO:LavoroDTOInsert,session:Session):
    """Aggiorna il lavoro che trova nel db"""
    #Controllo su input funzione
    verify_int(id)
    verify_lavoro(lavoroDTO)
    verify_session(session)
    #Query
    lavoro_update=session.scalar(select(Lavoro).where(Lavoro.id==id))
    if(lavoro_update):
        lavoro_update.id_commessa=lavoroDTO.id_commessa
        lavoro_update.id_risorsa=lavoroDTO.id_risorsa
        lavoro_update.ore_lavoro=lavoroDTO.ore_lavoro
        lavoro_update.data_lavoro=lavoroDTO.data_lavoro
        lavoro_update.luogo_di_lavoro=lavoroDTO.luogo_di_lavoro
        lavoro_update.descrizione_lavoro=lavoroDTO.descrizione_lavoro

        session.commit()

        return LavoroDTORead.lavoro_to_DTO(lavoro_update)

    else:
        raise Exception("Lavoro non trovato nel db")

def updateCommessa(id:int,commessaDTO:CommessaDTOInsert,session:Session):
    verify_int(id)
    verify_commessa(commessaDTO)
    verify_session(session)

    commessa_update=session.scalar(select(Commessa).where(Commessa.id==id))
    if(commessa_update):
        commessa_update.nome_commessa=commessaDTO.nome_commessa
        commessa_update.inizio_commessa=commessaDTO.inizio_commessa
        commessa_update.fine_commessa=commessaDTO.fine_commessa
        commessa_update.stato_commessa=commessaDTO.stato_commessa
        commessa_update.note_commessa=commessaDTO.note_commessa
        session.commit()

        return CommessaDTORead.commessa_to_DTO(commessa_update)

    else:
        raise Exception("Commessa non trovata nel db")
        



def updateAssenza(id:int,assenzaDTO:AssenzaDTOInsert,session:Session):
    """Aggiorna il lavoro che trova nel db"""
    #Controllo su input funzione
    verify_int(id)
    verify_assenza(assenzaDTO)
    verify_session(session)
    #Query
    assenza_update=session.scalar(select(Assenza).where(Assenza.id==id))
    if(assenza_update):
        assenza_update.tipo_assenza=assenzaDTO.tipo_assenza
        assenza_update.durata_assenza=assenzaDTO.durata_assenza
        assenza_update.data_assenza=assenzaDTO.data_assenza
        assenza_update.note_assenza=assenzaDTO.note_assenza
        session.commit()

        return AssenzaDTORead.assenza_to_DTO(assenza_update)

    else:
        raise Exception("Assenza non trovata nel db")

def deleteLavoroById(id:int,session:Session):
    verify_int(id)
    verify_session(session)

    lavoro=session.scalar(select(Lavoro).where(Lavoro.id==id))
    if(lavoro):
        session.delete(lavoro)
        session.commit()
        return LavoroDTORead.lavoro_to_DTO(lavoro)
    else:
        raise Exception("Lavoro non trovato nel db")
    
def deleteAssenzaById(id:int,session:Session):
    verify_int(id)
    verify_session(session)

    assenza=session.scalar(select(Assenza).where(Assenza.id==id))
    if(assenza):
        session.delete(assenza)
        session.commit()
        return AssenzaDTORead.assenza_to_DTO(assenza)
    else:
        raise Exception("Assenza non trovata nel db")
    
def deleteCommessaById(id:int,session:Session):
    verify_int(id)
    verify_session(session)

    if session.scalar(select(Lavoro).where(Lavoro.id_commessa==id)):
        raise Exception("Non è possibile eliminare la commessa")
    
    commessa=session.scalar(select(Commessa).where(Commessa.id==id))
    if(commessa):
        session.delete(commessa)
        session.commit()
        return CommessaDTORead.commessa_to_DTO(commessa)
    else:
        raise Exception("Commessa non trovata nel db")

def deleteRisorsaById(id:int,session:Session):
    verify_int(id)
    verify_session(session)

    if session.scalar(select(Lavoro).where(Lavoro.id_risorsa==id)):
        raise Exception("Non è possibile eliminare la risorsa")
    
    risorsa=session.scalar(select(Risorsa).where(Risorsa.id==id))
    if(risorsa):
        session.delete(risorsa)
        session.commit()
        return RisorsaDTORead.risorsa_to_DTO(risorsa)
    else:
        raise Exception("Risorsa non trovata nel db")