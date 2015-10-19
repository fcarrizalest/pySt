from ..core import db

group_users = db.Table(
    'user_group',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('group.id')))


class Group(db.Model):

	__tablename__ = 'group'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True)


class User(db.Model):

	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255) , unique=True )
	password = db.Column(db.String(120))
	active = db.Column(db.Boolean())
	groups = db.relationship('Group', secondary=group_users,
                            backref=db.backref('user', lazy='dynamic'))

