from . import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

#TODO make timeout a part of config, in seconds
USER_TIMEOUT = 30

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    avatar = db.Column(db.String())
    last_seen = db.Column(db.Integer, default=lambda: datetime.utcnow().timestamp())

    def ping(self):
        self.last_seen = datetime.utcnow().timestamp()

    @hybrid_property
    def is_active(self):
         return self.last_seen > datetime.utcnow().timestamp() - USER_TIMEOUT

    def to_json(self):
        return {
            'userId': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'lastSeen': self.last_seen
        }

    def __repr__(self):
        return 'User {0}'.format(self.username)


class Room(db.Model, SerializerMixin):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    room_type = db.Column(db.String(50))
    capacity = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return 'Room {0}'.format(self.name)


class UserLocation(db.Model, SerializerMixin):
    __tablename__ = 'user_locations'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    def __repr__(self):
        return 'User {0} is in Room {1}'.format(self.user_id, self.room_id)


class UserRoomState(db.Model, SerializerMixin):
    __tablename__ = 'user_room_states'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    discovered = db.Column(db.Boolean)

    def __repr__(self):
        visited = 'visited' if self.discovered else 'not visited'
        return 'User {0} has {1} Room {2}'.format(self.user_id, visited, self.room_id)
