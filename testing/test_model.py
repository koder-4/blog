from model import Session, User, Article, Comment, Tag, insert_test_data
from pytest import fixture


# creating the database once
@fixture(scope="class")
def session():
    insert_test_data()
    return Session()


class TestModel:
    def test_users_count(self, session):
        # check, that have 4 users
        assert session.query(User).count() == 4

    def test_articles_count(self, session):
        # check, that have 3 articles
        assert session.query(Article).count() == 3

    def test_comments_count(self, session):
        # check, that have 4 comments
        assert session.query(Comment).count() == 4

    def test_tag_count(self, session):
        # check, that have 3 tags
        assert session.query(Tag).count() == 3

    def test_have_user_gates(self, session):
        # check, that Bill Gates is in users
        assert session.query(User).filter_by(username='Bill Gates').one_or_none() is not None

    def test_have_user_doe(self, session):
        # check, that we have 2 users, whose names ends with "doe"
        assert session.query(User).filter(User.username.like('%doe')).count() == 2

    def test_john_doe_has_article(self, session):
        # check, that John Doe wrote 2 articles
        author = session.query(User).filter_by(username='John Doe').one()
        articles = session.query(Article).filter_by(
            author=author.id
        ).all()

        assert articles is not None
        assert len(articles) == 2
        assert 'Python' in [article.header for article in articles]
        assert 'Python on linux' in [article.header for article in articles]

    def test_have_articles_about_python(self, session):
        # check, that we have 3 articles tagged "python"
        tag = session.query(Tag).filter_by(tag='python').one()
        articles = tag.articles
        assert len(articles) == 3
        assert 'Python' in [article.header for article in articles]
        assert 'Python on windows' in [article.header for article in articles]
        assert 'Python on linux' in [article.header for article in articles]

    def test_have_articles_about_windows(self, session):
        # check, that we have 1 article tagged "windows"
        tag = session.query(Tag).filter_by(tag='windows').one()
        articles = tag.articles
        assert len(articles) == 1
        assert 'Python on windows' in [article.header for article in articles]
