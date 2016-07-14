
from nucleus.app import DB

class User(DB.Model):
	__tablename__ = 'users'

	id = DB.Column(DB.Integer, primary_key=True)
	email = DB.Column(DB.String(128))
	fname = DB.Column(DB.String(128))
	lname = DB.Column(DB.String(128))
	status = DB.Column(DB.String(255))
	created = DB.Column(DB.DateTime)
	class_standing = DB.Column(DB.String(255))
	major = DB.Column(DB.String(255))
	shirt_size = DB.Column(DB.String(255))
	dietary_restrictions = DB.Column(DB.String(255))
	birthday = DB.Column(DB.Date)
	gender = DB.Column(DB.String(255))
	phone_number = DB.Column(DB.String(255))
	school = DB.Column(DB.String(255))
	special_needs = DB.Column(DB.Text)
	checked_in = DB.Column(DB.Boolean)
	# roles = DB.relationship('Role', secondary='user_roles', backref=DB.backref('users', lazy='dynamic'))
	access_token = DB.Column(DB.String(255))

	def __init__(self, dict):
		self.email = dict['data']['email']
		self.phone_number = '123456'
		self.class_standing = 'hello'

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)