from database import Database
from models.blog import Blog
from models.post import Post
from colorama import Fore, Back, Style

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
        desciption = input("Enter description title: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=desciption)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):

        """ User read or write blogs? """
        print("Would you like to \
                \n\tread " + Fore.BLUE + "(R)" + Style.RESET_ALL + " blogs \
                \n\twrite " + Fore.BLUE + "(W)" + Style.RESET_ALL + " blogs \
                \n\tmanage " + Fore.BLUE + "(M)" + Style.RESET_ALL + " blogs \
                \n\tQuit " + Fore.BLUE + "(Q)" + Style.RESET_ALL + " program\n")
        option = input("Enter here: ")

        if option == 'R' or option == 'r':
            self._list_blogs()
            self._view_blogs()
        elif option == 'W' or option == 'w':
            self.user_blog.new_post()
        elif option == 'M' or option == 'm':
            self._manage_blogs()
        elif option == 'Q' or option == 'q':
            quit()
        else:
            print("Thanks aHAhaHA! Try again! AHAhaHA!")

    def _list_blogs(self):
        blogs = Database.find(collection='blogs', query={})
        for blog in blogs:
            print("\nID: {}, Title: {}, Author: {}".format(blog['id'], blog['title'], blog['author']))
        print('\n')

    def _view_blogs(self):
        blog_to_see = input("Enter the ID of the blog you want to read: ")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("\nDate: {}  |  ID: {}\nTitle: {}\n\n{}".format(post['date'], post['id'],
                                                                  post['title'], post['content']))
        print('\n')

    def _manage_blogs(self):
        # enter ID for which blog to manage:
        self._list_blogs()
        blog_to_manage = input("Enter the ID of the blog you want to manage: ")
        # get posts
        blog = Blog.from_mongo(blog_to_manage)
        posts = blog.get_posts()
        for post in posts:
            print("\nDate: {}  |  ID: {}\nTitle: {}\n".format(post['date'],
                                                              post['id'],
                                                              post['title']))
        # prompt user for ID of post to manage
        post_id = input("Enter the ID of the post you would like to manage: ")
        post = Post.from_mongo(post_id)
        # prompt user for delete (del) or move (mv) post:
        option = input("Choose to delete (del) or move (mv) this post: ")
        # if (del):
        if option == "del" or option == "DEL":
            print("*DELETE*")
            Database.DATABASE['blogs'].delete_one({'id': post})
        #    delete post
        # if (mv):
        if option == "mv" or option == "MV":
            print("Listing blogs:\n")
            self._list_blogs()
            destination_id = input("Enter the ID of the blog you want to move this post to: ")
            print("*MOVE*")
            # move post to destination
            # del post from source location
            pass
