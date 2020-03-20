# @Time    : 2020/3/19 3:59 下午
# @Author  : yym
# @Site : 
# @File    : sql_scripts.py
# @Software: PyCharm

# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,DateTime,Enum,UniqueConstraint,ForeignKey,Table
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

ConParams = "mysql+pymysql://root:lingren@93@192.168.0.93/db,Charset:utf8"
Base = declarative_base()   #实例化基类

user_more_host = Table(
    'user_more_host',Base.metadata,
    Column('user_profile_id',Integer,ForeignKey('user_profile.id')),
    Column('bind_id',Integer,ForeignKey('bind.id'))
)         ##多对多关联

group_more_host = Table(
    'group_more_host',Base.metadata,
    Column('bind_id',Integer,ForeignKey('bind.id')),
    Column('host_group_id',Integer,ForeignKey('host_group.id'))
)         ##多对多关联

user_more_group = Table(
    'user_more_group',Base.metadata,
    Column('user_profile_id',Integer,ForeignKey('user_profile.id')),
    Column('host_group_id',Integer,ForeignKey('host_group.id'))
)         ##多对多关联

class hosts(Base):
    '''
    定义用户表结构
    '''
    __tablename__ = 'hosts'
    id = Column(Integer,primary_key=True)
    hostname = Column(String(32),unique=True)
    ip = Column(String(64),unique=True)
    port = Column(Integer,default=22)
    # remote_user = relationship('remote_user',secondary=host_remoteuser,backref='hosts')   #外键关联
    def __repr__(self):
        return self.hostname

class user_profile(Base):
    '''
    定义堡垒机用户表结构
    '''
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),unique=True)
    password = Column(String(128))
    binds = relationship('bind',secondary='user_host',backref='user_profile')
    group_host = relationship('host_group',secondary='user_more_group',backref='user_profile')
    def __repr__(self):
        return self.name


class remote_user(Base):
    '''
    定义服务器用户表结构
    '''
    __tablename__ = 'remote_user'
    __table_args__ = (UniqueConstraint('auth_type','name','password',name = '_user_password_uc_'))       #联合唯一
    AuthType = [
        ('ssh_password','ssh/password'),
        ('ssh_key','ssh/key')]
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(128))
    # auth_type = Column(Enum(0,1))
    auth_type = Column(ChoiceType(AuthType))

    def __repr__(self):
        return self.name

class host_group(Base):
    '''
    定义服务器组表结构
    '''
    __tablename__ = 'host_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),unique=True)
    bind_host = relationship('bind',secondary='group_more_host',backref='host_group')

    def __repr__(self):
        return self.name
class auditlog(Base):
    '''
    定义日志表结构
    '''
    ___tablename__ = 'auditlog'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    user = Column(String(32))
    cmd = Column(String(128))
    ip = Column(String(32))
    remote_user = Column(String(32))

class bind(Base):
    '''
    实现三表关联
    主机，用户，分组
    '''
    __talbename__ = 'bind'
    __table_args__ = (UniqueConstraint('id','host_id','group_id',name = '_id_host_group_'))     #联合唯一
    id = Column(Integer,primary_key=True)
    host_id = Column(Integer,ForeignKey('hosts.id'))
    # group_id = Column(Integer,ForeignKey('host_group.id'))
    remote_user_id = Column(Integer,ForeignKey('remote_user.id'))
    host = relationship('hosts',backref='bind_hosts')
    # group = relationship('host_group',backref = 'bind_group_id')
    remote = relationship('remote_user',backef = 'bind_remote_user')
    def __repr__(self):
        return "< %s -- %s -- %s >" % (
            self.host.ip,
            self.remote.name,
            self.group.name,
        )