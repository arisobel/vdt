# -*- coding: utf-8 -*-

def calc_dias_uteis(ano, mes, fj=[], fl=[], dias_aula=[]):

    from datetime import  date
    import calendar
    ult_dia = calendar.monthrange(ano, mes)[1]
    d1 = date(ano, mes, 1)
    d2 = date(ano, mes, ult_dia)
    dias_uteis = {}

    count = 0

    for d_ord in range(d1.toordinal(), d2.toordinal()+1):
        d = date.fromordinal(d_ord)
        if dias_aula:
            if date(ano, mes, d.day).weekday() in dias_aula:
                if (d.day not in fl) and  (d.day not in fj):
                    count += 1
                    dias_uteis[d.day]=d.weekday()
        else:
            if (d.weekday() in [i for i in range(0,5)]):
                if (d.day not in fl) and  (d.day not in fj):
                    count += 1
                    dias_uteis[d.day]=d.weekday()

    return dias_uteis

# sicroniza a tabela n para n de media_tag com o campo tags, para facilitar os buscas
def atualiza_tags(s, f=None):
    linha = s.select().first()
    media_id = linha.id
    #colcoa todas as tags como inativas
    db(db.media_tag.media_id == media_id).update(ativo=False)
    if linha.tags:
        for tag in linha.tags:
            # atualiza cada tag na tabela n para n
            db.media_tag.update_or_insert((db.media_tag.media_id == media_id) & (db.media_tag.tag_id==tag),
                                       media_id=media_id,
                                       tag_id=tag,
                                       ativo = True
                                         )
    return False

# sicroniza a tabela n para n de media_tag com o campo tags, para facilitar os buscas
def cria_media_tags(s, i):
    linha = db(db.media_video.id==i).select().first()
    media_id = i
    #colcoa todas as tags como inativas
    db(db.media_tag.media_id == media_id).update(ativo=False)
    if linha.tags:
        for tag in linha.tags:
            # atualiza cada tag na tabela n para n
            db.media_tag.update_or_insert((db.media_tag.media_id == media_id) & (db.media_tag.tag_id==tag),
                                       media_id=media_id,
                                       tag_id=tag,
                                       ativo = True
                                         )
    return False


def conta_views(id_media):
    total=0
    #conta os votos
    views = db.media_view.media_id.count()
    tot_views=  db((db.media_view.media_id==id_media)).select(views.with_alias("views"), 
                                                       groupby=db.media_view.user_id|db.media_view.user_ip)
    if tot_views:
       for view in tot_views:
            total+=1

    return total
