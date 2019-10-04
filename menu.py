
from database import Database
from models.blog import Blog
from models.post import Post
from colorama import Fore, Style  # coloring text in terminal, add 'Back' for text background colors

__author__ = 'chansen'


class Menu(object):

    def __init__(self):
        self.user = input("Enter author name: ")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back, {}!".format(self.user))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = Database.find_one('blogs', {'author': self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter description title: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):

        """ User read or write blogs? """
        print("Would you like to \
                \n\tread " + Fore.BLUE + "(R)" + Style.RESET_ALL + " blogs \
                \n\twrite " + Fore.BLUE + "(W)" + Style.RESET_ALL + " blogs \
                \n\tmanage " + Fore.BLUE + "(M)" + Style.RESET_ALL + " blogs \
                \n\tquit " + Fore.BLUE + "(Q)" + Style.RESET_ALL + " program\n")
        option = input("Enter here: ").lower()

        if option in ['read', 'r']:
            self._list_blogs()
            self._read_blog()
        elif option in ['write', 'w']:
            self.user_blog.new_post()
        elif option in ['manage', 'm']:
            self._manage_blogs()
        elif option in ['quit', 'q']:
            quit()
        else:
            print("Thanks aHAhaHA! Try again! AHAhaHA!")

    @staticmethod
    def _list_blogs():
        blogs = Database.find(collection='blogs', query={})
        print("Listing blogs from all of our very distinguished authors:\n")
        for blog in blogs:
            print("\nID: {}, Title: {}, Author: {}".format(blog['id'], blog['title'], blog['author']))
        print('\n')

    @staticmethod
    def _read_blog():
        blog_to_see = input("Enter the ID of the blog you want to read: ")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("\nDate: {}  |  ID: {}\nTitle: {}\n\n{}".format(post['date'], post['id'],
                                                                  post['title'], post['content']))
        print('\n')

    @staticmethod
    def _delete_post(post):
        option = input("Are you sure you want to delete this post? (Y/N): ").lower()
        if option == 'y' or option == 'yes':
            x = Database.delete_one('posts', {'id': post})
            print(x.deleted_count, " document(s) deleted")

    @staticmethod
    def _move_post(post_id):
        destination_id = input("Enter the ID of the blog you want to move this post to: ")
        # change 'blog_id' to match the blog that was selected
        Database.DATABASE['posts'].update_one({'id': post_id},
                                              {'$set': {'blog_id': destination_id}})

    def _manage_blogs(self):
        self._list_blogs()
        blog_to_manage = input("Enter the ID of the blog you want to manage: ")
        blog = Blog.from_mongo(blog_to_manage)
        if blog:
            posts = blog.get_posts()
            for post in posts:
                print("\nDate: {}  |  ID: {}\nTitle: {}\n".format(post['date'], post['id'], post['title']))
            post_id = input("Enter the ID of the post you would like to manage: ")
            post = Post.from_mongo(post_id)
            if post:
                option = input("Choose to delete (del) or move (mv) this post: ")
                if option == "del" or option == "DEL":
                    self._delete_post(post_id)
                if option == "mv" or option == "MV":
                    self._list_blogs()
                    self._move_post(post_id)
