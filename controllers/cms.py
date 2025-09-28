# -*- coding: utf-8 -*-
def index():
    crs = db((db.conteudo.tipo=="CR")&(db.conteudo.ativo==True)).select()
    return dict(crs=crs)
