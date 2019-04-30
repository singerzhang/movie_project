# coding:utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员信息
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, comment="昵称")  # 昵称
    pwd = db.Column(db.String(100), comment="密码")  # 密码
    email = db.Column(db.String(100), unique=True, comment="邮箱")  # 邮箱
    phone = db.Column(db.String(11), unique=True, comment="手机")  # 手机
    info = db.Column(db.Text(), comment="个性简介")  # 个性简介
    face = db.Column(db.String(255), unique=True, comment="头像")  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow(), comment="添加时间")  # 添加时间
    uuid = db.Column(db.String(255), unique=True, comment="唯一标志符")  # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系
    comments = db.relationship('Comment', backref='user')  # 评论外键
    moviecols = db.relationship('Moviecol', backref='user')  # 收藏外键

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100), comment="登录ip")
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, comment="标签名称")  # 昵称
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影外键

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True, comment="电影名称")  # 标题
    url = db.Column(db.String(255), unique=True, comment="地址")  # 地址
    info = db.Column(db.Text(), comment="电影简介")  # 简介
    logo = db.Column(db.String(255), unique=True, comment="封面")  # 封面
    star = db.Column(db.SmallInteger, comment="星级")  # 星级
    playnum = db.Column(db.BigInteger, comment="播放量")  # 播放量
    commentnum = db.Column(db.BigInteger, comment="评论数量")  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255), comment="上映地区")  # 上映地区
    release_time = db.Column(db.Date, comment="上映时间")  # 上映时间
    length = db.Column(db.String(100), comment="播放时间")  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 电影外键
    moviecols = db.relationship('Moviecol', backref='movie')  # 收藏外键

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True, comment="电影名称")  # 标题
    logo = db.Column(db.String(255), unique=True, comment="封面")  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    info = db.Column(db.Text(), comment="评论内容")  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, comment="权限名称")  # 标题
    url = db.Column(db.String(255), unique=True, comment="地址")  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, comment="角色名称")  # 标题
    auths = db.Column(db.String(600), comment="权限列表")  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, comment="管理员账号")  # 管理员账号
    pwd = db.Column(db.String(100), comment="密码")  # 密码
    is_super = db.Column(db.SmallInteger, comment="是否超级管理员")  # 是否为超级管理员,0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员日志外键关系
    oplogs = db.relationship('Oplog', backref='admin')  # 操作日志外键关系

    def __repr__(self):
        return "<Admin %r>" % self.name


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100), comment="登录ip")  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100), comment="登录IP")  # 登录ip
    reason = db.Column(db.String(600), comment="操作原因")  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now(), comment="添加时间")  # 添加时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == '__main__':
    db.create_all()

