import util
from constant_blog import TITLE, RESULT, PAYLOAD


def main():
    blog_posts = util.fetch_data(util.JSON_DATA_PATH)[PAYLOAD]

    print(list(sorted(blog_posts, key = lambda x: x[TITLE], reverse=True)))


if __name__ == '__main__':
    main()
