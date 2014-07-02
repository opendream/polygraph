
from fabric.api import lcd, local

def prepare_deployment(branch_name='master'):
    local('python manage.py test')
    local('git add -p && git commit')

def deploy():
    with lcd('/web/polygraph/source/polygraph/'):

        # With git...
        local('git pull /web/polygraph/source/polygraph/')

        # With both
        #local('python manage.py migrate domain')
        local('python manage.py test')
        local('/web/polygraph/source/polygraph/restart')
