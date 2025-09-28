# -*- coding: utf-8 -*-
# tente algo como
def index():
    from urllib.parse import urlsplit, parse_qs
    url_arquivo = ""
    idd = request.args(0)
    link, tipo_media, spotify_episode, url_arquivo, yt_episode = "", "", "", "", ""
    resenha, lng = "", {}
    nome_palestrantre, foto_palestrantre, titulo = "", "", ""
    comentarios = []
    response.logo_img = 'logo_vdt_player.png'
    response.title = "Player"
    if idd:
        video = db(db.media_video.id==idd).select().first()
        #comentarios = db(db.coment_media.media_id==idd).select(orderby=~db.coment_media.criado_em)

        #legendas anexas
        lista_legendas = []

        db_legendas = db(db.legenda.media_video==idd).select()
        if db_legendas:
            for lg in db_legendas:
                lista_legendas.append({'srt': lg.arquivo, 'lingua': lg.lingua })

            lng ={k:v for k,v in  linguas}

        #conta os votos
        votos = db.vote_media.id.count()
        tot_votos=  db((db.vote_media.media_id==idd)&(db.vote_media.ativo==True)).select(votos.with_alias("votos"),
                                                           db.vote_media.vote_type.with_alias("tipo"),
                                                           groupby=db.vote_media.vote_type)

        dict_votos = {'bomb':'lightning-charge-fill',
                      'heart':'heart',
                      'must':'asterisk',
                      'like':'hand-thumbs-up',
                      }


        palestrante = video.palestrante
        #carrega dados do palestrante
        db_plastrante = None
        if palestrante:
            db_plastrante = db(db.palestrante.id==palestrante).select().first()
            nome_palestrantre = db_plastrante.nome
            foto_palestrantre = db_plastrante.foto

        url_arquivo = video.arquivo
        link = video.link
        tipo_media = video.tipo_media
        resenha = video.resenha
        titulo =  video.titulo
        time_uploaded = video.lancado
        if tipo_media == 'S':
            # Exemplo de URL
            spotify_url = link
            # Parseando a URL
            parsed_url = urlsplit(spotify_url)
            caminho = parsed_url.path
            spotify_episode = caminho.split("/")[-1]

        elif tipo_media == 'YT':
            # Exemplo de URL
            url = link
            # Parseando a URL
            parsed_url = urlsplit(url)
            caminho = parsed_url.path
            query = parsed_url.query
            yt_episode = "{}?{}".format(caminho, query)


        # conta visualização, caso naoo for audio ou video internos
        if tipo_media not in ('V', 'A'):
            id_view = db.media_view.insert(media_id=idd)


    return dict(message="hello from toca.py",
                url_arquivo=url_arquivo,
               link = link,
               tipo_media = tipo_media,
               spotify_episode=spotify_episode,
               yt_episode=yt_episode,
               resenha = resenha,
               nome_palestrantre=nome_palestrantre,
               foto_palestrantre=foto_palestrantre,
               titulo=titulo,
               lista_legendas=lista_legendas,
               lng=lng,
               tot_votos=tot_votos,
               dict_votos=dict_votos,
               time_uploaded=time_uploaded,
               #comentarios=comentarios,
               )

#===========================================
# BS"D
# 2024-01-25
# pega o shiur de uma lista aleatória
#===========================================
def random_shiur():
    import random
    shiur = db(db.media_video.aprovacao=="A").select().sort(lambda row: random.random())

    id_shiur = shiur[0].id

    return redirect(URL('toca','index', args=[id_shiur]))

#===========================================
# BS"D
# 2024-03-07
# pega os shiurim postados desdde domingo da
# semana corrente
#===========================================
def lista_da_semana():
    import datetime
    # Obter a data de hoje
    data_atual = datetime.date.today()
    # Encontrar o dia da semana (0 = segunda-feira, 6 = domingo)
    dia_da_semana = data_atual.weekday()
    # Subtrair o número de dias que faltam até domingo
    domingo = data_atual - datetime.timedelta(days=dia_da_semana)
    domingo = domingo - datetime.timedelta(days=1)
    dt_str_domingo = domingo.strftime("%d-%m-%Y")

    return redirect(URL('media','shiurim', vars={'desde':dt_str_domingo}))


#===========================================
# BS"D
# 2024-03-07
# pega os shiurim postados desdde domingo da
# semana corrente
#===========================================
def selecao_da_semana():
    import datetime
    # Obter a data de hoje
    data_atual = datetime.date.today()
    # Encontrar o dia da semana (0 = segunda-feira, 6 = domingo)
    dia_da_semana = data_atual.weekday()
    # Subtrair o número de dias que faltam até domingo
    domingo = data_atual - datetime.timedelta(days=dia_da_semana)
    domingo = domingo - datetime.timedelta(days=1)
    dt_str_domingo = domingo.strftime("%d-%m-%Y")

    return redirect(URL('media','shiurim', vars={'desde':dt_str_domingo,'tag':11}))




#===========================================
# BS"D
# 2024-01-25
# pega o shiur de uma lista aleatória
#===========================================
def lista_coments():
    idd = request.args(0)
    coments = db(db.coment_media.media_id==idd).select(orderby=~db.coment_media.criado_em)

    return dict(coments=coments)


#===========================================
# BS"D
# 2024-01-30
# teste com a API do youtuvbe framework para
# registrar se o player ta tocando
#===========================================
def toca_yt():
    return dict()


#===========================================
# BS"D
# 2024-01-30
# teste com a API do youtuvbe framework para
# registrar se o player ta tocando
#===========================================
def toca_yt_new():
    return dict()


#===========================================
# BS"D
# 2024-02-05
# votação de shiur
# registrar se o player ta tocando
#===========================================
def vote():
    id_media = request.args(0)
    voto = request.args(1)
    user_id = auth.user_id
    user_ip = request.client

    # caso o usuário estiver cadastrado e logado
    # atualiza conforme user_id e media_id
    if user_id:
        # tenta carregar o voto
        voto_db = db(
                (db.vote_media.media_id==id_media)&(db.vote_media.user_id==user_id)&(db.vote_media.vote_type==voto)
               ).select().first()
        # caso o voto exista, inverte o valor do ativo
        if voto_db:
            voto_db.update_record(ativo = not voto_db.ativo)
        else:
            db.vote_media.update_or_insert((db.vote_media.user_id == user_id) & (db.vote_media.media_id == id_media),
                                   media_id=id_media,
                                   user_id=user_id,
                                   vote_type=voto,
                                   ativo=True)
    #caso o user nao estiver logado
    else:
        voto_db = db(
                (db.vote_media.media_id==id_media)&(db.vote_media.voter_ip==user_ip)&(db.vote_media.vote_type==voto)
               ).select().first()
        # caso o voto exista, inverte o valor do ativo
        if voto_db:
            voto_db.update_record(ativo = not voto_db.ativo)
        else:
            db.vote_media.update_or_insert((db.vote_media.voter_ip == user_ip) & (db.vote_media.media_id == id_media),
                                   media_id=id_media,
                                   voter_ip=user_ip,
                                   vote_type=voto,
                                   ativo=True
                                          )

    #db((db.vote_media.media_id==id_media)&(
    #id_voto = db.vote_media.insert(media_id=id_media, vote_type=voto)
    db.commit()
    #tot_votos=  len(db((db.vote_media.media_id==id_media)&(db.vote_media.ativo==True)).select())

    return 0

#===========================================
# BS"D
# 2024-02-06
# carrega os votos
#===========================================
def load_votes():
    media_id = request.args(0)
    #conta os votos
    votos = db.vote_media.id.count()
    tot_votos=  db((db.vote_media.media_id==media_id)&(db.vote_media.ativo==True)).select(votos.with_alias("votos"),
                                                       db.vote_media.vote_type.with_alias("tipo"),
                                                       groupby=db.vote_media.vote_type)

    dict_votos = {'bomb':'lightning-charge-fill',
                  'heart':'heart',
                  'must':'asterisk',
                  'like':'hand-thumbs-up',
                  }
    div_container = DIV()

    if tot_votos:
       total=0
       for voto in tot_votos:
            icone = TAG.i(_class="bi bi-{}".format(dict_votos[voto.tipo]))
            div_container.append(icone)
            total+=voto.votos
       tot = SPAN(total,_class="badge badge-info")
       div_container.append(tot)
    else:
        icone = TAG.i(_class="bi bi-{}".format(dict_votos['like']))
        div_container.append(icone)

    return div_container




#===========================================
# BS"D
# 2024-03-06
# carrega os views
#===========================================
def load_views():
    media_id = request.args(0)
    div_container = DIV()

    '''
    #conta os votos
    views = db.media_view.media_id.count()
    tot_views=  db((db.media_view.media_id==media_id)).select(views.with_alias("views"),
                                                       groupby=db.media_view.user_id|db.media_view.user_ip)
    total=0
    if tot_views:
       for view in tot_views:
            total+=1
    '''
    total = conta_views(media_id)

    icone = TAG.i(_class="bi bi-eye")
    tot = SPAN(total,_class="badge badge-info")
    div_container.append(tot)
    div_container.append(icone)



    return div_container


def stream_video():
    import os
    url_arquivo = request.args(0)
    #path_to_video = URL('uploads', args=url_arquivo)
    path_to_video = os.path.join(request.env.web2py_path, "applications","init","static","files", url_arquivo)

    range_header = request.env.http_range
    if not range_header:
        raise HTTP(416, "Range not satisfiable")

    size = os.path.getsize(path_to_video)
    start, end = range_header.replace('bytes=', '').split('-')
    start = int(start)
    end = int(end) if end else size - 1

    with open(path_to_video, 'rb') as f:
        f.seek(start)
        data = f.read(end - start + 1)

    response.headers['Content-Range'] = f'bytes {start}-{end}/{size}'
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['Content-Length'] = str(end - start + 1)
    response.headers['Content-Type'] = 'video/mp4'

    return data

def teste_stream():
    idd_video = request.args(0)
    video_db = db(db.media_video.id==idd_video).select().first()
    url_arquivo = video_db.arquivo

    return dict(url_arquivo=url_arquivo)
