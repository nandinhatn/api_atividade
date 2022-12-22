from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades
import json

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):

#pega os dados
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome =nome).first()

        try:
            response = {
            'nome': pessoa.nome,
            'idade': pessoa.idade,
            'id': pessoa.id
            }

        except AttributeError:
            response={
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response
#altera os dados

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados :
            pessoa.nome= dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()

        response ={
            'id': pessoa.id,
            'nome':pessoa.nome,
            'idade': pessoa.idade

        }
        return response
    def delete(self,nome):
        pessoa = Pessoas.query.filter_by(nome= nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return {'status': 'sucesso',
                'mensagem': mensagem
                }




class Pessoas_All(Resource):

    def get(self):
        pessoas= Pessoas.query.all()
        response =[{'id':i.id, 'nome':i.nome,'idade':i.idade} for i in pessoas]


        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'],idade = dados['idade'])
        pessoa.save()
        response ={ 'nome': pessoa.nome,
                    'idade': pessoa.idade,
                    'id': pessoa.id


        }
        return response


class ListaAtividades(Resource):

    def get(self):
        atividades= Atividades.query.all()
        response =[{'pessoa': i.pessoa.nome, 'nome':i.nome,'id': i.id} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome= dados['nome'],pessoa= pessoa)
        atividade.save()
        response ={
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id':atividade.id
        }
        return response




api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(Pessoas_All, '/pessoa/')
api.add_resource(ListaAtividades, '/atividade/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
