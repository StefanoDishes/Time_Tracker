from sqlalchemy import String,Integer,ForeignKey,SmallInteger,Float,LargeBinary,Column,func,DateTime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,declarative_base

from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Risorsa(Base):
    __tablename__="risorse"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    nome_utente:Mapped[str] = mapped_column("nome",String(128))
    cognome_utente:Mapped[str] = mapped_column("cognome",String(128))
    email_utente:Mapped[str] = mapped_column("mail",String(128))
    password_utente:Mapped[str] = mapped_column("password",String(255), nullable=False)
    tipo_utente:Mapped[str]=mapped_column("tipoUtente",String(15))
    stato_utente:Mapped[int] = mapped_column("attivo",SmallInteger)

    assenze:Mapped[List["Assenza"]]=relationship()
    lavori:Mapped[List["Lavoro"]]=relationship()

    def __repr__(self):
        return f"Risorsa(nome_utente={self.nome_utente!r},cognome_utente={self.cognome_utente!r},email_utente={self.email_utente!r},password_utente={self.password_utente!r},tipo_utente={self.tipo_utente!r},stato_utente={self.stato_utente})"

class Commessa(Base):
    __tablename__="commesse"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    nome_commessa:Mapped[str]=mapped_column("commessa",String(128))
    inizio_commessa:Mapped[int]=mapped_column("inizio",SmallInteger)
    fine_commessa:Mapped[int]=mapped_column("fine",SmallInteger)
    stato_commessa:Mapped[str]=mapped_column("stato",String(6))
    note_commessa:Mapped[str]=mapped_column("note",String(255))

    lavoro:Mapped[List["Lavoro"]]=relationship

    def __repr__(self):
        return f"Commessa(nome_commessa={self.nome_commessa!r},inizio_commessa={self.inizio_commessa!r},fine_commessa={self.fine_commessa!r},stato_commessa={self.stato_commessa!r},note_commessa={self.note_commessa!r})"
    
class Assenza(Base):
    __tablename__="ferie_malattia"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    id_utente:Mapped[int]=mapped_column("risorsa",Integer,ForeignKey(Risorsa.id))
    tipo_assenza:Mapped[str]=mapped_column("tipo",String(8))
    durata_assenza:Mapped[int]=mapped_column("durata",SmallInteger)
    data_assenza:Mapped[str]=mapped_column("data",String(10))
    note_assenza:Mapped[str]=mapped_column("note",String(128))
    data_immissione:Mapped[datetime]=mapped_column("data_immissione",DateTime(),default=func.now())

    def __repr__(self):
        return f"Assenza(id_utente={self.id_utente!r},tipo_assenza={self.tipo_assenza!r},durata_assenza={self.durata_assenza!r},data_assenza={self.data_assenza!r},note_assenza={self.note_assenza!r},data_immissione={self.data_immissione})"

class Lavoro(Base):
    __tablename__="dati"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    id_risorsa:Mapped[int]=mapped_column("risorsa",Integer,ForeignKey(Risorsa.id),nullable=True)
    id_commessa:Mapped[int]=mapped_column("commessa",Integer,ForeignKey(Commessa.id),nullable=True)
    ore_lavoro:Mapped[float]=mapped_column("ore",Float)
    data_lavoro:Mapped[str]=mapped_column("data",String(10))
    luogo_di_lavoro:Mapped[str]=mapped_column("luogo",String(20))
    descrizione_lavoro:Mapped[str]=mapped_column("note",String(255))
    data_immissione:Mapped[datetime]=mapped_column("data_immissione",DateTime(),default=func.now())

    def __repr__(self):
        return f"Lavoro(id_risorsa={self.id_risorsa!r},id_commessa={self.id_commessa!r},ore_lavoro={self.ore_lavoro!r},data_lavoro={self.data_lavoro!r},luogo_di_lavoro={self.luogo_di_lavoro!r},descrizione_lavoro={self.descrizione_lavoro},data_immissione={self.data_immissione!r})"