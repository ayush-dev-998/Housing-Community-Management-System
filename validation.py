import threading
import time

class User:
    def __init__(self, name):
        self.name = name

    def update(self, article, blog_writer):
        print(f'For {self.name}, new article {article} by {blog_writer.name} is added')

class BlogWriter:
    def __init__(self, name):
        self.name = name
        self.__subscribers = []
        self.__articles = []
        self.lock = threading.Lock()  # Add a lock for thread safety

    def add_article(self, article):
        with self.lock:
            self.__articles.append(article)
            self.notify_subscribers(article)

    def subscribe(self, subscriber):
        with self.lock:
            self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        with self.lock:
            self.__subscribers.remove(subscriber)

    def notify_subscribers(self, article):
        with self.lock:
            for sub in self.__subscribers:
                sub.update(article, self)

def user_thread(blog_writer, user, articles):
    for article in articles:
        time.sleep(1)  # Simulate some time passing
        blog_writer.add_article(article)

if __name__ == '__main__':
    blog_writer = BlogWriter('Hardik\'s blog')
    shailaja = User('Shailaja')
    aarav = User('Aarav')

    blog_writer.subscribe(shailaja)
    blog_writer.subscribe(aarav)

    articles_writer_thread = threading.Thread(target=user_thread, args=(blog_writer, shailaja, ['Article 1', 'Article 2']))
    articles_writer_thread.start()

    articles_reader_thread = threading.Thread(target=user_thread, args=(blog_writer, aarav, ['Article 3', 'Article 4']))
    articles_reader_thread.start()

    articles_writer_thread.join()
    articles_reader_thread.join()
