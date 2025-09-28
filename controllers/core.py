# -*- coding: utf-8 -*-
# tente algo como
def trata_pres():


    id_pessoa = request.args(0)
    data_aula = str(request.args(1))
    hora = str(request.args(2))
    aula = int(request.args(3))
    id_pres = request.args(4) or None
    hora_fim = request.args(5) or None


    if data_aula:
        data_aula = datetime.strptime(data_aula,"%Y-%m-%d").strftime("%d-%m-%Y")

    if hora:
        hora = "%s:00" % hora.replace("_",":").replace("_",":")

    if hora_fim:
       hora_fim = "%s:00" % hora_fim.replace("_",":").replace("_",":")
    else:
       hora_fim = None
    
    if  int(id_pres or "0")>0:
        if hora_fim:
            ret = db(db.presenca.id==id_pres).validate_and_update(pessoa=id_pessoa,horario=hora,dia=data_aula,aula=aula, horario_fim=hora_fim)
        else:
            ret = db(db.presenca.id==id_pres).validate_and_update(pessoa=id_pessoa,horario=hora,dia=data_aula,aula=aula)
    else:
        if hora_fim:
            ret = db.presenca.validate_and_insert(pessoa=id_pessoa,horario=hora,dia=data_aula,aula=aula,horario_fim=hora_fim)
        else:
            ret = db.presenca.validate_and_insert(pessoa=id_pessoa,horario=hora,dia=data_aula,aula=aula)
        #ret = db.presenca.validate_and_insert(pessoa=3,horario="20:00:00",dia="2021-11-12",aula=2)
        db.commit()
        id_pres=ret.id

    botao = """<span data-id="{id_pres}" aluno-id="{id_pessoa}" class="btn-aluno-del btn btn-danger">
               <i class="fa fa-times-circle"></i>
               </span>""".format(id_pres=id_pres, id_pessoa=id_pessoa)
    
    retorno = ret.id or id_pres
    #return response.json(dict(erro=erro ,id_pres=id_pres, pessoa=id_pessoa,horario=hora,dia=data,aula=aula))
    return response.json(dict(ret=retorno))
    #return retorno
    
def del_pres():
    
    id_pres = request.args(0)
    ret = dict(erros="nao deletado", retorno="Invalido")
    
    try:
        db(db.presenca.id==id_pres).delete()
        ret = dict(erros="", retorno="OK")
    except:
        pass

    
    return response.json(ret)

def search_pessoa():
    if not request.vars.search: return ''
    
    term = request.vars.search
    alunos = {"{} {}".format(row['first_name'], row['last_name']):row['id'] for row in db((db.auth_user.first_name.contains(term))|(db.auth_user.last_name.contains(term))).select() }
    
    return  DIV(*[DIV(k,
                     _onclick="window.location = '%s'" % URL('pessoa','index', args=[alunos[k]]),
                     _onmouseover="this.style.backgroundColor='yellow'",
                     _onmouseout="this.style.backgroundColor='white'"
                     ) for k in alunos])
