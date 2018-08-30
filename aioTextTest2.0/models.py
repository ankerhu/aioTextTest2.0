import time,uuid
from orm import Model,StringField,BooleanField,FloatField,TextField

def next_id():
	return '%015d%s000' % (int(time.time() * 1000),uuid.uuid4().hex)

class User(Model):
	__table__ = 'users'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	openid = StringField(ddl = 'varchar(255)')
	session_key = StringField(ddl = 'varchar(255)')
	sessionId = StringField(ddl = 'varchar(255)')
	feedback = TextField()
	create_at = FloatField(default = time.time)

class Examination(Model):
	__table__ = 'examinations'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	name = StringField(ddl='varchar(50)')

class Title(Model):
	__table__ = 'titles'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	name = StringField(ddl='varchar(50)')
	exam_id = StringField(ddl='varchar(50)')
	content = TextField()

class Question(Model):
	__table__ = 'questions'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	title_id = StringField(ddl='varchar(50)')
	content = TextField()
	markReference = TextField()

class Mark(Model):
	__table__ = 'marks'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	user_mark_id = StringField(ddl='varchar(50)')
	user_answer_id = StringField(ddl='varchar(50)')
	question_id = StringField(ddl='varchar(50)')
	markNumByUser = FloatField(default=0.0)
	markNumByMachine = FloatField(default=0.0)
	create_at = FloatField(default = time.time)

class Answer(Model):
	__table__ = 'answers'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	answerText = TextField()
	question_id = StringField(ddl='varchar(50)')
	user_id = StringField(ddl='varchar(50)')