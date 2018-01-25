from pymodm import MongoModel, fields

class Detalhes(MongoModel):
	quantidade_diarias = fields.FloatField()
	valor_diaria = fields.FloatField()
	tipo_passagem = fields.CharField()


class Viagem(MongoModel):
	inicio = fields.DateTimeField()
	termino = fields.DateTimeField()
	assunto = fields.CharField()
	destino = fields.CharField()
	deputado = fields.CharField()
	is_cancelada = fields.BooleanField(default=False)
	situacao = fields.CharField()
	detalhes = fields.EmbeddedDocumentField(Detalhes)