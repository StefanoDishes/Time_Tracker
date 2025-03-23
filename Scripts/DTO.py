from dataclasses import dataclass
import datetime
from Scripts.Entities import Risorsa,Commessa,Assenza,Lavoro
from Scripts.Validation_Data import verify_mail,verify_str,verify_int,verify_float
from typing import Optional
from typing import List

@dataclass
class RisorsaDTOInsert():
    email_utente:str
    password_utente:str
    nome_utente:Optional[str] = None
    cognome_utente:Optional[str] = None
    tipo_utente:str = "risorsa"
    stato_utente:int = 1
    
    def DTO_validation(self) -> bool :
        if(verify_mail(self.email_utente) and verify_str(self.nome_utente,self.cognome_utente,self.email_utente,self.password_utente,self.tipo_utente) and verify_int(self.stato_utente)):
            return True
        else:
            return False

    def DTO_to_risorsa(self) -> Risorsa|None:
        if(self.DTO_validation()):
            return Risorsa(nome_utente=self.nome_utente,cognome_utente=self.cognome_utente,email_utente=self.email_utente,password_utente=self.password_utente,tipo_utente=self.tipo_utente,stato_utente=self.stato_utente)
        else:
            return None 

@dataclass
class RisorsaDTORead():
    id:int
    email_utente:str
    tipo_utente:str
    stato_utente:int
    nome_utente:Optional[str] = None
    cognome_utente:Optional[str] = None
    #Potrei esporre in una lista tutte le attività e assenze dell'utente
    #lista_lavori:Optional[List[Lavoro]]=None
    #lista_assenze:Optional[List[Assenza]]=None

    @staticmethod
    def risorsa_to_DTO(risorsa:Risorsa) :
        return RisorsaDTORead(id=risorsa.id,nome_utente=risorsa.nome_utente,cognome_utente=risorsa.cognome_utente,email_utente=risorsa.email_utente,tipo_utente=risorsa.tipo_utente,stato_utente=risorsa.stato_utente)

@dataclass
class CommessaDTOInsert():
    nome_commessa:str
    inizio_commessa:int = datetime.datetime.now().year
    stato_commessa:str = "aperta"
    fine_commessa:Optional[int] = None
    note_commessa:Optional[str] = None

    def DTO_validation(self) -> bool:
        if(verify_str(self.nome_commessa,self.stato_commessa,self.note_commessa) and verify_int(self.inizio_commessa,self.fine_commessa)):
            return True
        else:
            return False

    def DTO_to_commessa(self)->Commessa|None:
        if(self.DTO_validation()):
            return Commessa(nome_commessa=self.nome_commessa,inizio_commessa=self.inizio_commessa,fine_commessa=self.fine_commessa,stato_commessa=self.stato_commessa,note_commessa=self.note_commessa)
        else:
            return None

@dataclass
class CommessaDTORead():
    id:int
    nome_commessa:str
    inizio_commessa:int
    fine_commessa:Optional[int]
    stato_commessa:str
    note_commessa:Optional[str]
    
    @staticmethod
    def commessa_to_DTO(commessa:Commessa):
        return CommessaDTORead(id=commessa.id,nome_commessa=commessa.nome_commessa,inizio_commessa=commessa.inizio_commessa,fine_commessa=commessa.fine_commessa,stato_commessa=commessa.stato_commessa,note_commessa=commessa.note_commessa)

@dataclass
class AssenzaDTOInsert():
    id_utente:int
    tipo_assenza:str
    durata_assenza:int
    data_assenza:str
    note_assenza:Optional[str]=None

    def DTO_validation(self) -> bool:
        if(verify_str(self.tipo_assenza,self.data_assenza,self.note_assenza) and verify_int(self.id_utente,self.durata_assenza)):
            return True
        else:
            return False

    def DTO_to_assenza(self)->Assenza|None:
        if(self.DTO_validation()):
            return Assenza(id_utente=self.id_utente,tipo_assenza=self.tipo_assenza,durata_assenza=self.durata_assenza,data_assenza=self.data_assenza,note_assenza=self.note_assenza)
        else:
            return None

@dataclass
class AssenzaDTORead():
    tipo_assenza:str
    durata_assenza:int
    data_assenza:str

    @staticmethod
    def assenza_to_DTO(assenza:Assenza):
        return AssenzaDTORead(tipo_assenza=assenza.tipo_assenza,durata_assenza=assenza.durata_assenza,data_assenza=assenza.data_assenza)

@dataclass
class LavoroDTOInsert():
    id_risorsa:int
    id_commessa:int
    ore_lavoro:float
    data_lavoro:str
    luogo_di_lavoro:str
    descrizione_lavoro:Optional[str]=None

    def DTO_validation(self) -> bool:
        if(verify_str(self.data_lavoro,self.luogo_di_lavoro,self.descrizione_lavoro) and verify_int(self.id_risorsa,self.id_commessa) and verify_float(self.ore_lavoro)):
            return True
        else:
            return False

    def DTO_to_lavoro(self)->Lavoro|None:
        if(self.DTO_validation()):
            return Lavoro(id_risorsa=self.id_risorsa,id_commessa=self.id_commessa,ore_lavoro=self.ore_lavoro,data_lavoro=self.data_lavoro,luogo_di_lavoro=self.luogo_di_lavoro,descrizione_lavoro=self.descrizione_lavoro)
        else:
            return None

@dataclass
class LavoroDTORead():
    id_risorsa:int
    id_commessa:int
    ore_lavoro:float
    data_lavoro:str

    @staticmethod
    def lavoro_to_DTO(lavoro:Lavoro):
        return LavoroDTORead(id_risorsa=lavoro.id_risorsa,id_commessa=lavoro.id_commessa,ore_lavoro=lavoro.ore_lavoro,data_lavoro=lavoro.data_lavoro)
