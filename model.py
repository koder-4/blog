from datetime import datetime

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

DB_URL = 'sqlite:///blog.sqlite3'

engine = create_engine(url=DB_URL, echo=True)
Base = declarative_base(bind=engine)
metadata = MetaData()

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


articles_tags = Table('articles_tags', Base.metadata,
                      Column('tag_id', ForeignKey('tags.id')),
                      Column('article_id', ForeignKey('articles.id')))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    is_author = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    Articles = relationship("Article")
    Comments = relationship("Comment")


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)
    header = Column(String(200), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    tags = relationship("Tag", secondary=articles_tags, back_populates='articles')
    is_visible = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    Comments = relationship("Comment")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)
    article = Column(Integer, ForeignKey('articles.id'), nullable=False)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String(20), unique=True, nullable=False)
    articles = relationship("Article", secondary=articles_tags, back_populates="tags")


def insert_test_data():
    Base.metadata.drop_all()
    Base.metadata.create_all()

    session = Session()

    john = User(username='John Doe', password='123', is_author=True)
    jane = User(username='Jane Doe', password='1234', is_author=True)
    lucifer = User(username='Lucifer', password='666', is_author=False)
    gates = User(username='Bill Gates', password='coronavirus', is_author=False)

    for user in [john, jane, lucifer, gates]:
        session.add(user)

    session.commit()

    python = Tag(tag='python')
    linux = Tag(tag='linux')
    windows = Tag(tag='windows')

    for tag in [python, linux, windows]:
        session.add(tag)

    session.commit()

    python_linux = Article(author=john.id, header='Python on linux',
                           text='Using python on linux is awesome!!!', tags=[linux, python])
    python_windows = Article(author=jane.id, header='Python on windows',
                             text='Using python on windows is awesome to!!!', tags=[windows, python])
    python_awesome = Article(author=john.id, header='Python', text='Using python is awesome!!!', tags=[python])

    for article in [python_linux, python_windows, python_awesome]:
        session.add(article)

    session.commit()

    comments = [
        Comment(author=gates.id, article=python_linux.id, text='Never used linux, what is it?'),
        Comment(author=jane.id, article=python_linux.id, text='Going to write my own article'),
        Comment(author=lucifer.id, article=python_linux.id, text='Love linux, it has daemons and zombies!'),
        Comment(author=lucifer.id, article=python.id, text='Some comment, just to have them more then Gates has')
    ]

    for comment in comments:
        session.add(comment)

    session.commit()


def main():
    insert_test_data()


if __name__ == '__main__':
    main()
