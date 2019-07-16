from termcolor import colored
import shutil
from shutil import copyfile
# from otree.api import Page
from pgg._builtin import Page

def cp(*x, color='red', center=True):
    columns = shutil.get_terminal_size().columns
    x = ' '.join([str(i) for i in x])
    if center:
        x = x.center(columns, '-')
    print(colored(x, color, 'on_cyan', attrs=['bold']))


# TODO: move to management
def create_templates():
    from pgg.pages import page_sequence
    path = 'pgg/templates/pgg/'
    for p in page_sequence:
        if issubclass(p, Page):
            print(f'gonna create for {p.__name__}')
            copyfile(f'{path}MyPage.html', f'{path}{p.__name__}.html')
        else:
            print(f'NOT gonna create for {p.__name__}')


if __name__ == '__main__':
    create_templates()
