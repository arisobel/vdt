# -*- coding: utf-8 -*-
# tente algo como
def index():
    response.title = "Shiurim"
    categ = request.vars.categ or None
    paletrante = request.vars.palestr or None
    so_tops = True if request.vars.so_tops else False # se quiser apenas a listagem de tops
    eh_categ = True if request.vars.categ else False # se quiser apenas a listagem de tops
    eh_palest = True if paletrante else False # se quiser apenas a listagem de tops
    query = db.media_video


    # situação default
    searchable = True
    editable = True
    create = True
    cabec = "Lista de Shiurim - Geral"
    campos = [db.media_video.titulo,
                db.media_video.palestrante,
                db.media_video.categoria,
                db.media_video.eh_top,
                db.media_video.tipo_media,
                db.media_video.aprovacao,
                db.media_video.minutes,
                db.media_video.tags,
                db.media_video.lancado,
              ]


    if so_tops:
        searchable = False
        editable = False
        create = False
        query = (db.media_video.eh_top == True)
        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,

                  ]
        cabec = "Tops"


    if eh_categ:

        response.title = "Categoria {}".format(categ)
        searchable = False
        editable = False
        create = False
        query = (db.media_video.categoria == categ)

        categoria_db = db(db.categoria.id==categ).select().first()

        cabec = "Categoria {}".format(categoria_db['nome'].title())


        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,

                  ]
    if eh_palest:

        searchable = False
        editable = False
        create = False
        query = (db.media_video.palestrante == paletrante)
        palestrante_db = db(db.palestrante.id==paletrante).select().first()
        cabec = "{}".format(palestrante_db['nome'].title())
        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,

                  ]
        #db.palestrante.format  ="$(id)s"
        #db.media_video.palestrante.represent = lambda value, row: SPAN(IMG(_src=URL('default','download', args=str(value or "-|-").split("|")[1]), _class="img-circle", _width="60", _HEIGHT="80"  ), SPAN(value, _class="hidden-xs d-none d-sm-inline"))



    links = [
               dict(header='Play', body=lambda row: A(TAG.i(_class="icon icon-play bi bi-play"), _href =URL('toca','index',args=row.id), _class="btn  btn-default btn-secondary")),
               dict(header='Views', body=lambda row: SPAN(conta_views(row.id), _style="display: inline-block; width: 100%; text-align: center;"))

            ]

    form = SQLFORM.grid(query,
    	fields=campos,

        buttons_placement='left', # Botões a esquerda
        deletable = False,
        details=False, #desabilita a visualização
        searchable = searchable,
        editable = editable,
        create = create,
        #selectable=lambda ids : redirect(URL('artigo', 'action_multiple', vars=dict(id=ids))),
        #selectable_text="Selecione",
        headers = {'media_video.titulo': 'Nome do Shiur', 'media_video.tipo_media': 'Media'},
        orderby=[~db.media_video.lancado,~db.media_video.titulo],
        links = links,
        links_placement = 'left',
        #field_id= db.ARTIGOS.COD_ARTIGO,
        #field_id= ' ',
        maxtextlengths={'media_video.titulo':50, 'media_video.categoria':50,} ,
        showbuttontext=False, # Exibe os botões
        _class='web2py_grid',
    	csv=False)

    if request.args(-2) == 'new':
        redirect(URL('media','edit', args=0))

    elif request.args(-3) == 'edit':
       #redirect(URL('artigo_editar', vars= {'cod' : id_artigo} ))
       #redirect(URL('artigo_editar', args=[request.args(-1)]))
       idd = request.args(-1)
       redirect(URL('media','edit', args=idd ))

    return dict(
                form=form,
                so_tops=so_tops,
                cabec = cabec,
               )


@auth.requires_login()
def cards():
    # Check if current user has editores field set to True
    if not auth.user or not auth.user.editores:
        session.flash = "Acesso negado: Apenas editores podem visualizar os cartões."
        redirect(URL('default', 'index'))

    response.title = "Shiurim"
    categ = request.vars.categ or None
    paletrante = request.vars.palestr or None
    so_tops = True if request.vars.so_tops else False # se quiser apenas a listagem de tops
    eh_categ = True if request.vars.categ else False # se quiser apenas a listagem de tops
    eh_palest = True if paletrante else False # se quiser apenas a listagem de tops

    query = (db.media_video.eh_top == True)
    campos = [db.media_video.titulo,
                db.media_video.tipo_media,
                db.media_video.categoria,
                db.media_video.tags,
                db.media_video.id,
                db.media_video.resenha,
                db.palestrante.nome,
                db.palestrante.foto,

              ]
    lista = db(query).select(*campos, left=[db.palestrante.on(db.media_video.palestrante==db.palestrante.id)])

    return dict(lista=lista)

#=======================================
# lista de Tops
#
#=======================================
def lista():
    import random
    response.title = "TOP Shiurim"
    if request.args(0) == "short":
        response.title = "Short Shiurim"
    categ = request.vars.categ or None
    paletrante = request.vars.palestr or None
    so_tops = True if request.vars.so_tops else False # se quiser apenas a listagem de tops
    eh_categ = True if request.vars.categ else False # se quiser apenas a listagem de tops
    eh_palest = True if paletrante else False # se quiser apenas a listagem de tops

    if request.vars.l2:
        response.view ='media/lista2.html'
    else:
        response.view ='media/lista_tops.html'

    lista_selecao_semana = [r['media_id'] for r in  db(db.media_tag.tag_id==11).select()]

    query = (db.media_video.eh_top == True)|(db.media_video.id.belongs(lista_selecao_semana))

    if request.args(0):
        if request.args(0)=="short":
            query &= (db.media_video.minutes<=20)
    else:
        query &= (db.media_video.minutes>20)

    campos = [db.media_video.titulo,
                db.media_video.tipo_media,
                db.media_video.categoria,
                db.categoria.nome,
                db.media_video.tags,
                db.media_video.resenha,
                db.media_video.palestrante,
                db.media_video.tipo_media,
                db.media_video.tags,
                db.media_video.minutes,
                db.media_video.tag_chave,
                db.categoria.id,
                db.categoria.imagem,
                db.categoria.cor_fundo,
                db.categoria.fundo,
                db.media_video.id,
               db.palestrante.nome,
               db.palestrante.foto,

              ]
    lista = db(query).select(*campos,
                             left=[db.palestrante.on(db.media_video.palestrante==db.palestrante.id),
                                   db.categoria.on(db.media_video.categoria==db.categoria.id)
                                  ]).sort(lambda row: random.random())

    lista_ids_media = [r['media_video']['id'] for r in lista]

    lista_tags = db(db.media_tag.media_id.belongs(lista_ids_media)).select()

    dict_tags_nomes = {r['id']:r['nome'] for r in db(db.tag.id>0).select()}

    dict_tags = {}
    for tag in lista_tags:
        media_id = tag['media_id']
        if media_id not in dict_tags:
            dict_tags[media_id] = []
        dict_tags[media_id].append(dict_tags_nomes.get(tag['tag_id'],"-"))

    tipos_media = [("L","Link"),("V","Video"),("YT","Youtube"),("A","Audio"),("S","Spotify")]
    icons_media = [("L","link"),("V","camera-video-fill"),("YT","youtube"),("A","mic-fill"),("S","spotify")]

    dict_tipos_media =  {chave: valor for chave, valor in tipos_media}
    dict_icons_media =  {chave: valor for chave, valor in icons_media}

    dic_icon = {}
    for k,v in dict_icons_media.items():
        dic_icon[k] = CAT(SPAN(TAG.i(_class="bi bi-{}".format(dict_icons_media.get(k,"-"))), SPAN(dict_tipos_media.get(k,'-'),_class="ml-3 hidden-xs d-none d-sm-inline") ))


    return dict(lista=lista,
                dic_icon=dic_icon,
                dict_tags=dict_tags,
                lista_tags=lista_tags,
                lista_ids_media=lista_ids_media)





#=====================================================================
# funcao de criação e edição do conteúdo
#=====================================================================
@auth.requires_login()
def edit():
    user_ip = request.client
    # define os botões da aula / video
    buttons = [
        TAG.button('Salvar',_type="submit",_class = "btn btn-info pull-right"),
        A('Voltar a lista',_href=URL('media','index'),_class = "btn btn-default pull-right"),
        ]
    form_posts = ""
    try:
        idd = int(request.args(0) or "0")
    except:
        idd = 0

    #carrega grupos
    grupos = db(db.wa_group.id>0).select()


    if idd:

        form_video_editar = SQLFORM(db.media_video,idd,
                                          buttons =buttons,
                                          submit_button='Alterar',
                                          _id='form_video_editar' ,
                                          field_id='id'
                                          #field_id='COD_ARTIGO'
                                          )

        video = db(db.media_video.id==idd).select().first()
        if video.arquivo:
            form_video_editar.vars.url_arquivo = video.arquivo
        else:
            form_video_editar.vars.arquivo = 'Nenhuma imagem disponível'

        form_legendas = LOAD(c='media',
                     f='legendas_listar',
                     vars={'idd':idd},
                     content='Aguarde, carregando...',
                     target='lista_legendas',
                     ajax=True
                     )

        form_posts = LOAD(c='media',
                     f='postagens_listar',
                     vars={'idd':idd},
                     content='Aguarde, carregando...',
                     target='lista_postagens',
                     ajax=True
                     )


    else:
        form_video_editar = SQLFORM(db.media_video,
                                          buttons =buttons,
                                          submit_button='Incluir',
                                          field_id='id',
                                          #field_id='COD_ARTIGO',
                                          _id='form_video_editar')
        form_video_editar.vars.url_arquivo = ""
        form_legendas = "Primerio cadastre a Media"

    # coloca o campo resenha com 3 linhas
    form_video_editar.element(_name='resenha')['_rows'] = '3'

    #form_video_editar.custom.widget.arquivo = lambda field, value: SQLFORM.widgets.upload.widget(field, value, _accept='video/*')
    #form_video_editar.custom.widget.arquivo = lambda field, value, current: SQLFORM.widgets.upload.widget(field, value, _accept='video/*', uploadfolder=URL('uploads'))
    if form_video_editar.process().accepted:
        video_id = form_video_editar.vars.id
        session.flash = 'Efetuado com sucesso! ID {}'.format(video_id)
        return redirect(URL('media','edit', args=[video_id]))
        '''
        artigo_cod = form_artigo_editar.vars.f_codigo_art
        artigo_desc = form_artigo_editar.vars.f_descricao_art
        '''

    elif form_video_editar.errors:
        response.flash = 'Erro no Cadastro! %s  ' % (", \n".join(form_video_editar.errors))

    return dict(form_video_editar=form_video_editar,
                form_legendas=form_legendas,
                user_ip=user_ip,
                grupos=grupos,
                form_posts=form_posts)


def legendas_listar():

    id_legenda = request.vars.idd or "0"

    query = db.legenda.media_video==id_legenda
    db.legenda.media_video.default = id_legenda

    db.legenda.media_video.writable = False
    db.legenda.media_video.readable = False


    form_caps = SQLFORM.grid(query,
                             args=[id_legenda],
                             csv=False,
                             showbuttontext=False,
                             user_signature=False,
                             searchable=False)

    return dict(form_caps=form_caps)


# BH 2025-01-29 -- listagem das postagens das midias nos grupos

def postagens_listar():

    id_video = request.vars.idd or "0"

    query = db.media_post.media_id==id_video
    db.media_post.media_id.default = id_video

    db.media_post.media_id.writable = False
    db.media_post.media_id.readable = False

    fields = [db.media_post.post_time, db.media_post.wa_group]

    form_posts = SQLFORM.grid(query,
                             fields=fields,
                             args=[id_video],
                             csv=False,
                             create=False,
                             deletable=False,
                             editable=False,
                             details=False,
                             showbuttontext=False,
                             user_signature=False,
                             searchable=False)

    return dict(form_posts=form_posts)


def redir_top():

    id_categ = request.args(0)

    if id_categ:
        top_categ = db((db.media_video.categoria==id_categ)&(db.media_video.eh_top==True)).select(orderby=~db.media_video.id).first()
        if top_categ:
            id_media = top_categ['id']
            return redirect(URL('toca','index', args=[id_media]))

        else:
            return redirect(URL('media','index', vars={'categ':id_categ}))
    else:

        return redirect(URL('default','index'))

#============================================
# receber comentário
#============================================
def comentar():
    ret = 'nada'
    if request.vars:
        nome = request.post_vars.nome
        comentario = request.post_vars.coment
        media_id = request.args(0)

        ret = db.coment_media.validate_and_insert(media_id=media_id,
                                                  user_ip=request.client,
                                                 comentario=comentario,
                                                 nome_user=nome
                                                 )


    return ret


#==================================
# 2024-02-20 - sobel.ari
# contador de visualizações
#==================================

def views_count():
    media_id = request.args(0)
    id_view = 0
    if media_id:
        id_view = db.media_view.insert(media_id=media_id)

    return id_view


#==================================
# 2024-02-20 - sobel.ari
# contador de visualizações
#==================================

def shiurim():
    response.title = "Shiurim"
    categ = request.vars.categoria or None
    paletrante = request.vars.palestr or None
    so_tops = True if request.vars.so_tops else False # se quiser apenas a listagem de tops
    eh_categ = True if request.vars.categoria else False # se quiser apenas a listagem de tops
    eh_palest = True if paletrante else False # se quiser apenas a listagem de tops
    var = request.vars.var

    query = (db.media_video.aprovacao == "A")

    minutos = request.vars.minutos

    # controla a minutagem
    minuto_max = 0
    min_minuto = 0
    if minutos:
        if "-" in minutos:
            min_minuto, minuto_max = minutos.split("-")

    if not minuto_max:
        max_minuto = db.media_video.minutes.max()
        db_max_minuto = db(query).select( max_minuto.with_alias("maxminuto")).first()

        minuto_max = 50
        if db_max_minuto:
            minuto_max = db_max_minuto["maxminuto"]


    db_categorias = db(db.categoria).select()
    db_tags = db(db.tag).select()
    db_palestrantes = db(db.palestrante).select()

    if var:
        if var == "1":
            response.view = "media/shiurim1.html"

    #filtros
    minuto = request.vars.minutos or []
    if minuto:
        query &= (db.media_video.minutes>=min_minuto)
        query &= (db.media_video.minutes<=minuto_max)




    categs = request.vars.categ or []
    if categs:
        if isinstance(categs, list):
            query &= (db.media_video.categoria.belongs(categs))
        else:
            query &= (db.media_video.categoria==categs)
            categs = [categs]

    palests = request.vars.palest or []
    if palests:
        if isinstance(palests, list):
            query &= (db.media_video.palestrante.belongs(palests))
        else:
            query &= (db.media_video.palestrante==palests)
            palests = [palests]

    tags = request.vars.tag or []
    if tags:
        if isinstance(tags, list):
            # tags = [int(tag.replace("|","")) for tag in tags
            videos_tags = db(db.media_tag.tag_id.belongs(tags)).select()

        else:
            videos_tags = db(db.media_tag.tag_id==tags).select()
            #query &= (db.media_video.tags==tags)
            tags = [tags]

        videos_list = [r.media_id for r in videos_tags]
        query &= (db.media_video.id.belongs(videos_list))

    desde = request.vars.desde or ""
    if desde:
        formato = "%d-%m-%Y"
        dt_desde = datetime.strptime(desde, formato)
        query &= (db.media_video.lancado>=dt_desde)


    search = request.vars.search
    if search:
        query &= ((db.media_video.titulo.contains(search)))

    # situação default
    cabec = "Lista de Shiurim - Geral"
    campos = [db.media_video.titulo,
                db.media_video.palestrante,
                db.media_video.categoria,
                db.media_video.eh_top,
                db.media_video.tipo_media,
                db.media_video.aprovacao,
                db.media_video.tags,
                db.media_video.lancado,
                db.media_video.minutes,
                db.media_video.id,
                db.palestrante.foto,
                db.palestrante.nome,
                db.categoria.nome,
              ]


    if so_tops:
        query = (db.media_video.eh_top == True)
        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,
                    db.palestrante.foto,

                  ]
        cabec = "Tops"


    if eh_categ:

        response.title = "Categoria {}".format(categ)
        query = (db.media_video.categoria == categ)

        categoria_db = db(db.categoria.id==categ).select().first()

        cabec = "Categoria {}".format(categoria_db['nome'].title())


        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,
                    db.palestrante.foto,

                  ]
    if eh_palest:

        query = (db.media_video.palestrante == paletrante)
        palestrante_db = db(db.palestrante.id==paletrante).select().first()
        cabec = "{}".format(palestrante_db['nome'].title())
        campos = [db.media_video.titulo,
                    db.media_video.tipo_media,
                    db.media_video.categoria,
                    db.media_video.tags,
                    db.media_video.palestrante,
                    db.palestrante.foto,

                  ]


    listagem = db(query).select(*campos ,
                              left=[db.palestrante.on(db.media_video.palestrante==db.palestrante.id),
                                   db.categoria.on(db.media_video.categoria==db.categoria.id)
                                  ])

    ult_sql = db._lastsql[0]

    return dict(listagem=listagem,
                cabec=cabec,
                db_categorias=db_categorias,
                db_palestrantes=db_palestrantes,
                db_tags=db_tags,
                ult_sql=ult_sql,
                categs=categs,
                tags=tags,
                palests=palests,
                minuto_max=minuto_max,
                min_minuto=min_minuto,
                search=search,
               )

def chosen():
    return dict()

@auth.requires_login()
def kanban():
    """
    Kanban board view for media_video approval status
    """
    response.title = "Kanban - Status de Aprovação"

    # Get all media_video records with related data
    campos = [
        db.media_video.id,
        db.media_video.titulo,
        db.media_video.aprovacao,
        db.media_video.tipo_media,
        db.media_video.lancado,
        db.media_video.editor_responsavel,
        db.palestrante.nome,
        db.categoria.nome,
        db.auth_user.nome
    ]

    videos = db(db.media_video.id > 0).select(
        *campos,
        left=[
            db.palestrante.on(db.media_video.palestrante == db.palestrante.id),
            db.categoria.on(db.media_video.categoria == db.categoria.id),
            db.auth_user.on(db.media_video.editor_responsavel == db.auth_user.id)
        ],
        orderby=db.media_video.lancado
    )

    # Get approval statuses (defined in models/table.py but accessible here)
    aprovacoes = [("EP", "EM PROSPECÇÃO"),
                  ("AT","a Traduzir"),
                  ("TD","Traduzindo"),
                  ("RT","Revisando Tradução"),
                  ("PP","Pronto para publicar"),
                  ("PB","Publicado"),
                  ("AC","Arquivado / Catalogado"),
                  ("RC","Recusado | Somente VDT+"),
                  ("RT", "Recusado total"),
                  ("PV", "Perdemos o vídeo"),
                  ("P","Proposto"),
                  ("C","Curadoria"),
                  ("A","Aprovado")]

    tipos_media = [("L","Link"),("V","Video"),("YT","Youtube"),("A","Audio"),("S","Spotify")]

    # Get categories, speakers and editors for the add/edit card form
    categorias = db(db.categoria.id > 0).select(db.categoria.id, db.categoria.nome, orderby=db.categoria.nome)
    palestrantes = db(db.palestrante.id > 0).select(db.palestrante.id, db.palestrante.nome, orderby=db.palestrante.nome)
    # Get only users who are editors (editores = True)
    editores = db(db.auth_user.editores == True).select(db.auth_user.id, db.auth_user.nome, orderby=db.auth_user.nome)

    # Group videos by approval status
    kanban_data = {}
    for status_code, status_name in aprovacoes:
        kanban_data[status_code] = {
            'name': status_name,
            'videos': []
        }

    for video in videos:
        status = video['media_video']['aprovacao']
        if status in kanban_data:
            kanban_data[status]['videos'].append(video)

    return dict(kanban_data=kanban_data, aprovacoes=aprovacoes, tipos_media=tipos_media,
                categorias=categorias, palestrantes=palestrantes, editores=editores)

@auth.requires_login()
def kanban_update():
    """
    AJAX endpoint to update video approval status
    Requires user authentication
    """
    video_id = request.vars.video_id
    new_status = request.vars.new_status

    # Validate input parameters
    if not video_id or not new_status:
        return response.json({'success': False, 'message': 'Parâmetros inválidos'})

    # Valid approval statuses
    valid_statuses = ["EP", "AT", "TD", "RT", "PP", "PB", "AC", "RC", "PV", "P", "C", "A"]

    if new_status not in valid_statuses:
        return response.json({'success': False, 'message': 'Status de aprovação inválido'})

    try:
        # Check if video exists
        video = db(db.media_video.id == video_id).select().first()
        if not video:
            return response.json({'success': False, 'message': 'Vídeo não encontrado'})

        # Update the status
        db(db.media_video.id == video_id).update(aprovacao=new_status)
        db.commit()

        return response.json({
            'success': True,
            'message': 'Status atualizado com sucesso',
            'video_id': video_id,
            'new_status': new_status
        })

    except Exception as e:
        db.rollback()
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@auth.requires_login()
def kanban_get_card():
    """
    AJAX endpoint to get card data for editing
    Requires user authentication
    """
    video_id = request.vars.video_id

    if not video_id:
        return response.json({'success': False, 'message': 'ID do vídeo é obrigatório'})

    try:
        # Get video data with related information
        video = db(db.media_video.id == video_id).select(
            db.media_video.id,
            db.media_video.titulo,
            db.media_video.resenha,
            db.media_video.tipo_media,
            db.media_video.categoria,
            db.media_video.palestrante,
            db.media_video.link,
            db.media_video.aprovacao,
            db.media_video.editor_responsavel
        ).first()

        if not video:
            return response.json({'success': False, 'message': 'Vídeo não encontrado'})

        return response.json({
            'success': True,
            'data': {
                'id': video.id,
                'titulo': video.titulo or '',
                'resenha': video.resenha or '',
                'tipo_media': video.tipo_media or '',
                'categoria': video.categoria or '',
                'palestrante': video.palestrante or '',
                'link': video.link or '',
                'aprovacao': video.aprovacao or '',
                'editor_responsavel': video.editor_responsavel or ''
            }
        })

    except Exception as e:
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@auth.requires_login()
def kanban_edit_card():
    """
    AJAX endpoint to update an existing video card
    Requires user authentication
    """
    # Get form data
    video_id = request.vars.video_id
    titulo = request.vars.titulo
    resenha = request.vars.resenha
    tipo_media = request.vars.tipo_media
    categoria = request.vars.categoria
    palestrante = request.vars.palestrante
    link = request.vars.link
    aprovacao = request.vars.aprovacao
    editor_responsavel = request.vars.editor_responsavel

    # Validate required fields
    if not video_id:
        return response.json({'success': False, 'message': 'ID do vídeo é obrigatório'})

    if not titulo or not titulo.strip():
        return response.json({'success': False, 'message': 'Título é obrigatório'})

    if not tipo_media:
        return response.json({'success': False, 'message': 'Tipo de mídia é obrigatório'})

    # Valid approval statuses
    valid_statuses = ["EP", "AT", "TD", "RT", "PP", "PB", "AC", "RC", "PV", "P", "C", "A"]

    if aprovacao not in valid_statuses:
        return response.json({'success': False, 'message': 'Status de aprovação inválido'})

    # Valid media types
    valid_types = ["L", "V", "YT", "A", "S"]
    if tipo_media not in valid_types:
        return response.json({'success': False, 'message': 'Tipo de mídia inválido'})

    try:
        # Check if video exists
        video = db(db.media_video.id == video_id).select().first()
        if not video:
            return response.json({'success': False, 'message': 'Vídeo não encontrado'})

        # Prepare data for update
        data = {
            'titulo': titulo.strip(),
            'aprovacao': aprovacao,
            'tipo_media': tipo_media
        }

        # Add optional fields if provided
        data['resenha'] = resenha.strip() if resenha else None

        if categoria and categoria.strip():
            # Validate category exists
            cat = db(db.categoria.id == categoria).select().first()
            if cat:
                data['categoria'] = categoria
            else:
                data['categoria'] = None
        else:
            data['categoria'] = None

        if palestrante and palestrante.strip():
            # Validate speaker exists
            speaker = db(db.palestrante.id == palestrante).select().first()
            if speaker:
                data['palestrante'] = palestrante
            else:
                data['palestrante'] = None
        else:
            data['palestrante'] = None

        if editor_responsavel and editor_responsavel.strip():
            # Validate editor exists and has editores=True
            editor = db((db.auth_user.id == editor_responsavel) & (db.auth_user.editores == True)).select().first()
            if editor:
                data['editor_responsavel'] = editor_responsavel
            else:
                data['editor_responsavel'] = None
        else:
            data['editor_responsavel'] = None

        data['link'] = link.strip() if link else None

        # Update the video
        db(db.media_video.id == video_id).update(**data)
        db.commit()

        return response.json({
            'success': True,
            'message': 'Card atualizado com sucesso',
            'video_id': video_id
        })

    except Exception as e:
        db.rollback()
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@auth.requires_login()
def kanban_add_card():
    """
    AJAX endpoint to add a new video card
    Requires user authentication
    """
    # Get form data
    titulo = request.vars.titulo
    resenha = request.vars.resenha
    tipo_media = request.vars.tipo_media
    categoria = request.vars.categoria
    palestrante = request.vars.palestrante
    link = request.vars.link
    aprovacao = request.vars.aprovacao
    editor_responsavel = request.vars.editor_responsavel

    # Validate required fields
    if not titulo or not titulo.strip():
        return response.json({'success': False, 'message': 'Título é obrigatório'})

    if not tipo_media:
        return response.json({'success': False, 'message': 'Tipo de mídia é obrigatório'})

    # Valid approval statuses
    valid_statuses = ["EP", "AT", "TD", "RT", "PP", "PB", "AC", "RC", "PV", "P", "C", "A"]

    if aprovacao not in valid_statuses:
        return response.json({'success': False, 'message': 'Status de aprovação inválido'})

    # Valid media types
    valid_types = ["L", "V", "YT", "A", "S"]
    if tipo_media not in valid_types:
        return response.json({'success': False, 'message': 'Tipo de mídia inválido'})

    try:
        # Get or create a default tag for new cards
        default_tag = db(db.tag.nome == 'Kanban').select().first()
        if not default_tag:
            # Create default tag if it doesn't exist
            tag_id = db.tag.insert(nome='Kanban')
        else:
            tag_id = default_tag.id

        # Prepare data for insertion
        data = {
            'titulo': titulo.strip(),
            'aprovacao': aprovacao,
            'tipo_media': tipo_media,
            'tag_chave': tag_id,
            'criado_por': auth.user_id
        }

        # Add optional fields if provided
        if resenha and resenha.strip():
            data['resenha'] = resenha.strip()

        if categoria and categoria.strip():
            # Validate category exists
            cat = db(db.categoria.id == categoria).select().first()
            if cat:
                data['categoria'] = categoria

        if palestrante and palestrante.strip():
            # Validate speaker exists
            speaker = db(db.palestrante.id == palestrante).select().first()
            if speaker:
                data['palestrante'] = palestrante

        if editor_responsavel and editor_responsavel.strip():
            # Validate editor exists and has editores=True
            editor = db((db.auth_user.id == editor_responsavel) & (db.auth_user.editores == True)).select().first()
            if editor:
                data['editor_responsavel'] = editor_responsavel

        if link and link.strip():
            data['link'] = link.strip()

        # Insert the new video
        video_id = db.media_video.insert(**data)
        db.commit()

        return response.json({
            'success': True,
            'message': 'Card adicionado com sucesso',
            'video_id': video_id
        })

    except Exception as e:
        db.rollback()
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

@auth.requires_login()
def kanban_editores():
    """
    Kanban board view for distributing AT/TD cards to editors
    """
    # Check if current user has editores field set to True
    # if not auth.user or not auth.user.editores:
    if not auth.user:
        session.flash = "Acesso negado: Apenas editores podem visualizar o Kanban de Editores."
        redirect(URL('default', 'index'))

    response.title = "Kanban - Distribuição de Editores"

    # Get cards with AT and TD status
    campos = [
        db.media_video.id,
        db.media_video.titulo,
        db.media_video.aprovacao,
        db.media_video.tipo_media,
        db.media_video.lancado,
        db.media_video.editor_responsavel,
        db.palestrante.nome,
        db.categoria.nome,
        db.auth_user.nome
    ]

    # Filter for AT and TD cards only
    videos = db((db.media_video.aprovacao == "AT") | (db.media_video.aprovacao == "TD")).select(
        *campos,
        left=[
            db.palestrante.on(db.media_video.palestrante == db.palestrante.id),
            db.categoria.on(db.media_video.categoria == db.categoria.id),
            db.auth_user.on(db.media_video.editor_responsavel == db.auth_user.id)
        ],
        orderby=db.media_video.lancado
    )

    # Get all editors (users with editores=True)
    editores = db(db.auth_user.editores == True).select(
        db.auth_user.id,
        db.auth_user.nome,
        orderby=db.auth_user.nome
    )

    tipos_media = [("L","Link"),("V","Video"),("YT","Youtube"),("A","Audio"),("S","Spotify")]

    # Get categories and speakers for the modal form
    categorias = db(db.categoria.id > 0).select(db.categoria.id, db.categoria.nome, orderby=db.categoria.nome)
    palestrantes = db(db.palestrante.id > 0).select(db.palestrante.id, db.palestrante.nome, orderby=db.palestrante.nome)

    # Group videos by editor assignment
    kanban_data = {}

    # Unassigned column (no editor_responsavel)
    kanban_data['unassigned'] = {
        'name': 'Sem Editor Atribuído',
        'videos': []
    }

    # Create columns for each editor
    for editor in editores:
        kanban_data[f'editor_{editor.id}'] = {
            'name': editor.nome,
            'editor_id': editor.id,
            'videos': []
        }

    # Distribute videos into columns
    for video in videos:
        if video['media_video']['editor_responsavel']:
            editor_key = f"editor_{video['media_video']['editor_responsavel']}"
            if editor_key in kanban_data:
                kanban_data[editor_key]['videos'].append(video)
        else:
            kanban_data['unassigned']['videos'].append(video)

    return dict(kanban_data=kanban_data, editores=editores, tipos_media=tipos_media,
                categorias=categorias, palestrantes=palestrantes)

@auth.requires_login()
def kanban_editores_assign():
    """
    AJAX endpoint to assign/unassign editor to a video card
    """
    video_id = request.vars.video_id
    editor_id = request.vars.editor_id

    # Validate input parameters
    if not video_id:
        return response.json({'success': False, 'message': 'ID do vídeo é obrigatório'})

    try:
        # Check if video exists and is AT or TD
        video = db((db.media_video.id == video_id) &
                  ((db.media_video.aprovacao == "AT") | (db.media_video.aprovacao == "TD"))).select().first()
        if not video:
            return response.json({'success': False, 'message': 'Vídeo não encontrado ou não é AT/TD'})

        # If editor_id is provided, validate it's a real editor
        if editor_id and editor_id.strip():
            editor = db((db.auth_user.id == editor_id) & (db.auth_user.editores == True)).select().first()
            if not editor:
                return response.json({'success': False, 'message': 'Editor não encontrado'})

            # Assign editor
            db(db.media_video.id == video_id).update(editor_responsavel=editor_id)
            db.commit()

            return response.json({
                'success': True,
                'message': f'Card atribuído ao editor {editor.nome}',
                'video_id': video_id,
                'editor_id': editor_id,
                'editor_name': editor.nome
            })
        else:
            # Unassign editor (set to None)
            db(db.media_video.id == video_id).update(editor_responsavel=None)
            db.commit()

            return response.json({
                'success': True,
                'message': 'Editor removido do card',
                'video_id': video_id,
                'editor_id': None
            })
    except Exception as e:
        db.rollback()
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

def add_palestrante():
    """
    AJAX endpoint to add a new palestrante (speaker)
    Requires user authentication
    """
    nome = request.vars.nome

    # Validate required field
    if not nome or not nome.strip():
        return response.json({'success': False, 'message': 'Nome do palestrante é obrigatório'})

    nome = nome.strip()

    # Additional validation
    if len(nome) < 2:
        return response.json({'success': False, 'message': 'Nome muito curto (mínimo 2 caracteres)'})

    if len(nome) > 100:
        return response.json({'success': False, 'message': 'Nome muito longo (máximo 100 caracteres)'})

    # Check if palestrante already exists (case insensitive)
    existing = db(db.palestrante.nome.lower() == nome.lower()).select().first()
    if existing:
        return response.json({
            'success': True,
            'palestrante_id': existing.id,
            'nome': existing.nome,
            'message': 'Palestrante já existia'
        })

    try:
        # Insert new palestrante
        palestrante_id = db.palestrante.insert(nome=nome)
        db.commit()

        return response.json({
            'success': True,
            'palestrante_id': palestrante_id,
            'nome': nome,
            'message': 'Palestrante adicionado com sucesso'
        })

    except Exception as e:
        db.rollback()
        return response.json({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })

def postar_wa():

    import requests
    from requests.auth import HTTPBasicAuth

    id_grupo = request.args(1)
    gpid = request.args(2)
    link_video = request.args(3)
    id_video = request.args(0)

    # URL da API para enviar vídeo
    api_url = "https://zap.lion.app.br/send/video/"

    # Usuário e senha para autenticação
    username = 'liondata'
    password = 'brz050518'

    # URL do vídeo que será baixado e enviado
    video_url = "https://www.videosdetoire.com.br/init/default/download/{}".format(link_video)


    # muda o represent de categoria para nome_wa
    #db.media_video.categoria.represent = lambda value, row: row.nome_wa or ''

    db.categoria._format  = lambda r: r.nome_wa or ''


    # carrega o registro do video
    video_reg = db(db.media_video.id==id_video).select()

    vid = next(video_reg.render())

    palest = vid['palestrante']
    idioma = idiomas.get(vid['idioma'],"Desconhecida")
    legenda = idiomas.get(vid['legendas'],"Nenhuma")
    duracao = vid['duracao']
    titulo = vid['titulo']
    resenha = vid['resenha']
    categoria = vid['categoria']

    legendas = "Legendas em {}".format(legenda) if legenda != "Nenhuma" else ""

    if resenha:
        titulo = "{} \n {}".format(titulo, resenha)

    # forma descrição
    descric = '🗣 {idioma} {legendas}\n⏰ ± {duracao} min \n🎩 {palest} \n\n 💬 {titulo}'.format(idioma=idioma,duracao=duracao,palest=palest,titulo=titulo, legendas=legendas)

    if categoria:
        descric = "{} \n\n {}".format(categoria, descric)

    # Nome temporário do arquivo a ser salvo
    temp_video_file = "temp_video.mp4"

    # Baixar o vídeo da URL
    video_response = requests.get(video_url, stream=True)
    if video_response.status_code == 200:
        with open(temp_video_file, "wb") as f:
            for chunk in video_response.iter_content(1024):
                f.write(chunk)
        print("Download do vídeo concluído.")
    else:
        print("Falha ao baixar o vídeo.")


    # Dados do formulário exigidos pela API
    data = {
        'phone': '{}'.format(id_grupo),  # Número do destinatário ou ID do grupo
        'caption': descric,
        'view_once': 'false',
        'compress': 'false'
    }

    # Abrir e enviar o arquivo baixado
    with open(temp_video_file, "rb") as video_file:
        files = {
            'video': (temp_video_file, video_file, 'video/mp4')  # Nome do arquivo e MIME type
        }

        # Enviando a requisição POST
        resposta = requests.post(api_url, data=data, files=files, auth=HTTPBasicAuth(username, password))

    ret = {}
    # Verificação da resposta
    if resposta.status_code == 200:
        print("✅ Vídeo enviado com sucesso!")
        print(resposta.json())
        ret_j = resposta.json()
        id_message = ret_j['results']['message_id']
        id_post = db.media_post.insert(media_id=id_video, msg_id=id_message, wa_group=gpid)
        db.commit()
        ret['id_post'] = id_post
        ret.update(dict(media_id=id_video, msg_id=id_message, wa_grupo=gpid))
    else:
        print(f"❌ Falha ao enviar o vídeo. Status code: {response.status_code}")
        print("Resposta:", resposta.text)
        ret['erro'] =  resposta.text

    return response.json(ret)
