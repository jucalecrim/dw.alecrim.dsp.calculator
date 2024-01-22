import logging
# from datetime import datetime
# from acessobancomatrix.main import *
import pandas as pd
import json
import azure.functions as func
import dir_funcs.functions_padrao as funcs

banco = "ctar_hml"
#dbn = 'calc_tarif_base'


# body = {"data_ref": "02/2022", "id_ponto":"1", "tipo":"find"}
# body = {"data_ref": "02/2022", "campo_input": "juca luis", "id_ponto":"1", "tipo":"input"}


def acha_comentario(body):
    dbn = 'calc_tarif_trix'
    cred_ctar = funcs.loginSQL(dbn, banco)

    mes_ref = pd.to_datetime(body.get('data_ref')).month
    ano_ref = pd.to_datetime(body.get('data_ref')).year
    
    # query = "SELECT chave FROM calc_tarif_trix.tb_var_mensal WHERE id_ponto = {id_ponto} AND mes_ref = {mes_ref} AND ano_ref = {ano_ref}".format(id_ponto = body.get('id_ponto'), mes_ref = mes_ref, ano_ref = ano_ref)
    query = "SELECT sigla_ponto FROM tb_pts_trix WHERE id = {id_ponto}".format(id_ponto = body.get('id_ponto'))   
    aux_chave = cred_ctar.query(query, True)
    chave = aux_chave.sigla_ponto.iloc[0]  + "_" + str(ano_ref) + "_" + str(mes_ref)
    del query, aux_chave
    
    query = "SELECT campo_input FROM tb_comentario WHERE chave = '{}'".format(chave)
    aux_chave = cred_ctar.query(query, True)
    
    if aux_chave.shape[0] == 0:
        return ''
    else:       
        return aux_chave.campo_input.iloc[0]
        
def deleta_comentario(body):
    try:
        
        dbn = 'calc_tarif_trix'
        cred_ctar = funcs.loginSQL(dbn, banco)

        mes_ref = pd.to_datetime(body.get('data_ref')).month
        ano_ref = pd.to_datetime(body.get('data_ref')).year
        
        # query = "SELECT chave FROM calc_tarif_trix.tb_var_mensal WHERE id_ponto = {id_ponto} AND mes_ref = {mes_ref} AND ano_ref = {ano_ref}".format(id_ponto = body.get('id_ponto'), mes_ref = mes_ref, ano_ref = ano_ref)
        query = "SELECT sigla_ponto FROM tb_pts_trix WHERE id = {id_ponto}".format(id_ponto = body.get('id_ponto'))   
        aux_chave = cred_ctar.query(query, True)
        chave = aux_chave.sigla_ponto.iloc[0]  + "_" + str(ano_ref) + "_" + str(mes_ref)
        del query, aux_chave
        
        query = "SELECT id FROM tb_comentario WHERE chave = '{}'".format(chave)
        dt = cred_ctar.query(query, True)
        del_query = "DELETE FROM tb_comentario WHERE id = {}".format(dt.id.iloc[0])

        engine = cred_ctar.conectar()
        engine.execute(del_query)
        return 200
    except:
        return 404
        
def insere_comentario(body):
    try:
        
        dbn = 'calc_tarif_trix'
        cred_ctar = funcs.loginSQL(dbn, banco)
        
        mes_ref = pd.to_datetime(body.get('data_ref')).month
        ano_ref = pd.to_datetime(body.get('data_ref')).year
        
        # query = "SELECT chave FROM calc_tarif_trix.tb_var_mensal WHERE id_ponto = {id_ponto} AND mes_ref = {mes_ref} AND ano_ref = {ano_ref}".format(id_ponto = body.get('id_ponto'), mes_ref = mes_ref, ano_ref = ano_ref)
        query = "SELECT sigla_ponto FROM tb_pts_trix WHERE id = {id_ponto}".format(id_ponto = body.get('id_ponto'))   
        aux_chave = cred_ctar.query(query, True)
        chave = aux_chave.sigla_ponto.iloc[0]  + "_" + str(ano_ref) + "_" + str(mes_ref)
        del query, aux_chave
        
        query = "SELECT id FROM tb_comentario WHERE chave = '{}'".format(chave)
        dt = cred_ctar.query(query, True)
        
        if dt.shape[0] > 0:
            logging.info("Update comentário")
            end_query = "UPDATE tb_comentario SET campo_input = '{campo_input}' WHERE id = {id_pt}".format(campo_input = body.get('campo_input'), id_pt = dt.id.iloc[-1])
        else:
            logging.info("Insert comentário")
            end_query = "INSERT INTO tb_comentario (chave, campo_input) VALUES ('{chave}', '{campo_input}')".format(chave = chave, campo_input = body.get('campo_input'))

        engine = cred_ctar.conectar()
        engine.execute(end_query)
        return 200
    except:
        return 404
    
    
def main(req: func.HttpRequest) -> func.HttpResponse:
    body = json.loads(req.get_body())
    category = body.get("tipo")
    del body["tipo"]
    
    logging.info(body)
    logging.info(category)

    try:
        if category == "find":
            resp = acha_comentario(body)
            return func.HttpResponse(resp, status_code=200)
        else:
            if category == "input":
                resp = insere_comentario(body)
            elif category == "delete":
                resp = deleta_comentario(body)
            else:
                logging.exception("Body com formato inválido")
        
            logging.info(resp)
            return func.HttpResponse("Dado " + category + " OK!", status_code=200)

    except:
         return func.HttpResponse("Erro", status_code=404)
