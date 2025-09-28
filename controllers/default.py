# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from datetime import datetime
import calendar

def index():

    '''
    if not request.is_https:
        pass
    else:
        redirect(URL(c='default', f='index',scheme='http'))
    '''
    response.title = "VDT"
    crs = db((db.conteudo.tipo=="CR")&(db.conteudo.ativo==True)).select(orderby=db.conteudo.ordem) #tela_principal
    # mkt = db((db.conteudo.tipo=="MK")&(db.conteudo.ativo==True)).select(order_by=db.conteudo.ordem)
    if 'link' in (request.args(0) or ""):
        mkt = db((db.conteudo.tipo=="MK")&(db.conteudo.ativo==True)).select(orderby=db.conteudo.ordem)
    else:
        mkt = db((db.conteudo.tipo=="MK")&(db.conteudo.ativo==True)&(db.conteudo.tela_principal==True)).select(orderby=db.conteudo.ordem)
    ftr = db((db.conteudo.tipo=="FT")&(db.conteudo.ativo==True)).select()
    return dict(crs=crs, mkt=mkt, ftr=ftr)


def geral():
    import pytz

    if request.args(0):
        month, year = int(request.args(1)), int(request.args(0))
    else:
        year = int(datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y"))
        month = int(datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%m"))

    aulas = {r['id']:{'aula':r['nome'],'cor':r['cor'], 'hor':r['horario'], 'fim':r['fim'], 'dias':[int(s) for s in r['dias'].split(",")], 'executadas':0} for r in db(db.aula).select()}
    dic_presenca, dias_feriados = {},{}
    calend = calendar.monthcalendar(year, month)
    os_meses = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    calend = calendar.monthcalendar(year, month)
    anos = [n for n in range((int(year)-2),int(year+1))]
    meses = [n for n in range(1,13)]

    # feriados
    feriados_db = db((db.feriado.data_feriado.year()==year)&(db.feriado.data_feriado.month()==month)).select()
    if feriados_db:
        fj, fl, dias_feriados = [],[],{}
        for f in feriados_db:
            dia = int(f.data_feriado.day)
            dias_feriados[dia]=f

            if f.tipo=="JD":
                fj.append(dia)
            else:
                fl.append(dia)

    #presenca_mes = db((db.presenca.dia.year()==year)&(db.presenca.dia.month()==month)).select()
    count_dia = (db.presenca.id).count()
    presenca_mes = db((db.presenca.aula!=None)&(db.presenca.dia.year()==year)&(db.presenca.dia.month()==month)).select(
                       db.presenca.dia.with_alias("dia"),
                       db.presenca.aula.with_alias("aula"),
                       count_dia.with_alias("presencas"),
                       groupby=db.presenca.aula|db.presenca.dia
                      )
    feriados_db = db((db.feriado.data_feriado.year()==year)&(db.feriado.data_feriado.month()==month)).select()


    for p in presenca_mes:
        dia = p.dia.day
        aula= p.aula
        #periodos[aula].append(dia)
        if dia not in dic_presenca:
            dic_presenca[dia]={}
        dic_presenca[dia][aula]=p.presencas

    return dict(
                  presenca_mes=presenca_mes,
                  year=year,
                  month=month,
                  anos=anos,
                  meses=meses,
                  feriados_db=feriados_db,
                  os_meses=os_meses,
                  calend=calend,
                  dias_feriados=dias_feriados,
                  dic_presenca=dic_presenca,
                  aulas=aulas,
               )


@auth.requires_login()
def lista():
    #response.flash = T("Hello World")
    import pytz

    #hoje = datetime.today()
    agora = datetime.now()

    hoje = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d")
    hoje_frm = hoje
    aula_hoje = 1


    content = dict(
                   aula_hoje=aula_hoje,
                   hoje_frm=hoje_frm,
                   hoje=hoje,
                   agora=agora,
                  )

    return dict(message=T('Cadastros'), content=content)

# ===================
# valida presenca
# restringe se o dia a aula a o aluno ja estiverem sido marcados
# ===================

def valida_presenca(form):
    pessoa, aula, dia = form.vars.pessoa ,form.vars.aula, form.vars.dia
    reg = db((db.presenca.pessoa==pessoa)&(db.presenca.aula==aula)&(db.presenca.dia==dia)).select().first()
    if reg:
       form.errors.aula = 'Essa presença ja foi registrada'
    else:
       #form.errors.aula = 'Essa presença ja foi registrada pessoa {}, aula {} , dia{}'.format(pessoa, aula, dia)
       form.vars.aula = aula

    #se a distancia for maior que 1 Km, nao permite registrar
    #x, y = form.vars.geo_x, form.vars.geo_y
    #dist = calcula_dist(x,y)
    #if dist > 1:
    #   form.errors.aula = "Distancia do Shiur maior que a permitida para marcar presença"



@auth.requires_login()
def apontar_presenca():
    import pytz

    id_anot = int(request.args(0) or "0")

    agora = datetime.now(pytz.timezone('America/Sao_Paulo'))
    agora_hora = agora.strftime("%H:%M:%S")
    agora_flat = agora.strftime("%H%M")

    aulas = db(db.aula).select(orderby=db.aula.horario)

    for aula in aulas:
        ah = aula.horario
        hr = ah.strftime("%H%M")
        if int(agora_flat) > int(hr):
            res = "hr {} agora_flat {} agora_flat> hr {} aula.id {}".format(hr, agora_flat,  agora_flat> hr, aula.id )
            print(res)
            db.presenca.aula.default = aula.id



    dia_aula =  datetime.strptime(agora.strftime("%Y-%m-%d"),"%Y-%m-%d")
    user = auth.user_id
    user_db = db(db.auth_user.id==user).select().first()
    user_name = "{} {}".format(user_db['first_name'], user_db['last_name'])

    db.presenca.pessoa.default = user
    db.presenca.pessoa.requires = IS_IN_SET([(user, user_name)])
    db.presenca.dia.default = dia_aula
    db.presenca.horario.default = agora_hora

    #torna somente leitura
    #db.presenca.pessoa.writable = db.presenca.pessoa.readable =False
    db.presenca.doc_pago.writable = db.presenca.doc_pago.readable =False
    db.presenca.valor.writable = db.presenca.valor.readable =False
    db.presenca.horario_fim.writable = db.presenca.horario_fim.readable =False
    #db.presenca.dia.writable=False
    db.presenca.horario.writable=False


    # trasnforma geo loc em Somente Leitura, mas visivel no form
    if id_anot:
        form = SQLFORM(db.presenca,id_anot)
    else:
        form = SQLFORM(db.presenca)
    form.element(_name='geo_x')['_readonly'] = "readonly"
    form.element(_name='geo_y')['_readonly'] = "readonly"
    form.element(_name='dia')['_readonly'] = "readonly"
    # form.element(_name='pessoa')['_readonly'] = "readonly"



    if form.process(onvalidation=valida_presenca).accepted:
        redirect(URL('default','sucesso', args=form.vars.id ))
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'

    return dict(agora=agora, user=user, user_name=user_name, form=form)

@auth.requires_login()
def apontar_presenca_fim():
    import pytz

    id_anot = int(request.args(0) or "0")

    agora = datetime.now(pytz.timezone('America/Sao_Paulo'))
    agora_hora = agora.strftime("%H:%M:%S")
    agora_flat = agora.strftime("%H%M")

    aulas = db(db.aula).select(orderby=db.aula.horario)

    for aula in aulas:
        ah = aula.horario
        hr = ah.strftime("%H%M")
        if int(agora_flat) > int(hr):
            res = "hr {} agora_flat {} agora_flat> hr {} aula.id {}".format(hr, agora_flat,  agora_flat> hr, aula.id )
            print(res)
            db.presenca.aula.default = aula.id



    dia_aula =  datetime.strptime(agora.strftime("%Y-%m-%d"),"%Y-%m-%d")
    user = auth.user_id
    user_db = db(db.auth_user.id==user).select().first()
    user_name = "{} {}".format(user_db['first_name'], user_db['last_name'])

    db.presenca.pessoa.default = user
    db.presenca.pessoa.requires = IS_IN_SET([(user, user_name)])
    db.presenca.dia.default = dia_aula
    db.presenca.horario_fim.default = agora_hora

    #torna somente leitura
    #db.presenca.pessoa.writable = db.presenca.pessoa.readable =False
    db.presenca.doc_pago.writable = db.presenca.doc_pago.readable =False
    db.presenca.valor.writable = db.presenca.valor.readable =False
    #db.presenca.horario.writable =False
    #db.presenca.dia.writable=False
    #db.presenca.horario.writable=False


    # trasnforma geo loc em Somente Leitura, mas visivel no form
    if id_anot:
        form = SQLFORM(db.presenca,id_anot)
    else:
        form = SQLFORM(db.presenca)
    form.element(_name='geo_x')['_readonly'] = "readonly"
    form.element(_name='geo_y')['_readonly'] = "readonly"
    form.element(_name='dia')['_readonly'] = "readonly"
    form.element(_name='horario')['_readonly'] = "readonly"
    # form.element(_name='pessoa')['_readonly'] = "readonly"



    if form.process(onvalidation=valida_presenca).accepted:
        redirect(URL('default','sucesso', args=form.vars.id ))
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'

    return dict(agora=agora, user=user, user_name=user_name, form=form)



@auth.requires_login()
def sucesso():
    return dict()

@auth.requires_login()
def lista_presenca():

    aula_hoje = request.vars.qual_shiur or 1
    dia_aula =  request.vars.data_shiur or datetime.today()
    dia_mes_aula = str(dia_aula)[5:]

    #shiurim = db(db.aula).select()

    hora_aula_hj = db(db.aula.id==aula_hoje).select(db.aula.horario).first()['horario']

    alunos = db(db.auth_user.aulas.contains([aula_hoje])).select()
    presenca_db = db((db.presenca.aula==aula_hoje)& \
                  (db.presenca.pessoa.belongs([r['id'] for r in alunos])) & \
                  (db.presenca.dia==dia_aula)).select().as_dict()

    presenca = {presenca_db[p]['pessoa']:{**presenca_db[p]} for p in presenca_db}


    content = dict(shiurim=shiurim,
                   alunos=alunos,
                   presenca=presenca,
                   aula_hoje=aula_hoje,
                   hora_aula_hj=hora_aula_hj,
                   dia_aula=dia_aula,
                   dia_mes_aula=dia_mes_aula,
                  )

    return dict(content=content)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Smart Grid (example) -----
@auth.requires_login()
def grade():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename],  deletable=True)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
