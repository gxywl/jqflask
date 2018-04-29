# _*_ encoding: utf-8 _*_

'''
pip freeze > requirements.txt

'''

from fabric.api import local, env, run ,sudo ,cd

env.hosts=['deploy@192.168.1.14']
env.password='pub'

def test():
    local('python -m unittest discover')

def upgrade_libs():
    sudo("apt update")
    sudo("apt upgrade")

def setup():
    #test()
    #upgrade_libs()

    with cd("/home/deploy/websites/"):
        run("git clone https://github.com/gxywl/jqflask.git")

    with cd("/home/deploy/jqflask"):
        sudo("virtualenv /home/deploy/websites/jqflask/venv")
        sudo(". /home/deploy/websites/jqflask/venv/bin/activate")

        sudo('nano /home/deploy/websites/jqflask/venv/lib/python2.7/site.py')
        # _*_ encoding: utf-8 _*_
        # encoding = "ascii" ==> "utf8"

        run("/home/deploy/websites/jqflask/venv/bin/pip install -r requirements.txt")  #及uwsgi

        #run("python manage.py createdb")

        run("/home/deploy/websites/jqflask/venv/bin/uwsgi --ini /home/deploy/websites/jqflask/uwsgi.ini")

        sudo("cp superivsord.conf /etc/supervisor/conf.d/jqflask.conf") #先准备的命令
        sudo("cp nginx.conf /etc/nginx/sites-available/j.conf") #先准备的配置

        sudo("ln -s /etc/nginx/sites-available/j.conf /etc/nginx/sites-enabled/j.conf")  # 先准备的配置

    sudo('chown -R www-data:www-data /home/deploy/websites/jqflask')
    sudo('chmod -R 755 /home/deploy/websites/jqflask')

    sudo('service supervisor restart')
    sudo('service nginx restart')

    #sudo('client ')


def deploy():
    test()
    upgrade_libs()

    with cd('/home/deploy/websites/jqflask'):
        run("git pull")
        run("pip install -r requirements.txt")
