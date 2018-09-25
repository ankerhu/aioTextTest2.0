import time,uuid
from orm import Model,StringField,BooleanField,FloatField,TextField

def next_id():
	return '%015d%s000' % (int(time.time() * 1000),uuid.uuid4().hex)

#用户表
class User(Model):
	__table__ = 'users'
	#把session_key作为主键
	id = StringField(primary_key = True,default = next_id,ddl='varchar(255)')
	session_key = StringField(ddl = 'varchar(255)')
	nickName = StringField(ddl = 'varchar(255)')
	create_at = FloatField(default = time.time)

#反馈表
class Feedback(Model):
	__table__ = 'feedback'
	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	feedbackContent = TextField()
	userId = StringField(ddl='varchar(255)')
	nickName = StringField(ddl = 'varchar(255)')
	create_at = FloatField(default = time.time)

#考试表
class Examination(Model):
	__table__ = 'examinations'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	examName = StringField(ddl='varchar(50)')

#题干表
class Title(Model):
	__table__ = 'titles'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	titleName = StringField(ddl='varchar(50)')
	exam_id = StringField(ddl='varchar(50)')
	titleContent = TextField()

#题目表
class Question(Model):
	__table__ = 'questions'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	title_id = StringField(ddl='varchar(50)')
	questionContent = TextField()
	markReference = TextField()

#评分表
class Mark(Model):
	__table__ = 'marks'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	user_mark_id = StringField(ddl='varchar(50)')
	answer_id = StringField(ddl='varchar(50)')
	markNumByUser = FloatField(default=0.0)
	create_at = FloatField(default = time.time)

#答案表
class Answer(Model):
	__table__ = 'answers'

	id = StringField(primary_key = True,default = next_id,ddl='varchar(50)')
	answerText = TextField()
	question_id = StringField(ddl='varchar(50)')
	user_id = StringField(ddl='varchar(50)')
	markNumByMachine = FloatField(default=0.0)
	create_at = FloatField(default = time.time)