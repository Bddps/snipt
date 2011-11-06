import os

from fabric.api import local

def staticfiles():
    BASE_PATH = os.path.dirname(__file__)
    local('lessc %s/media/css/style.less %s/media/css/style.css' % (BASE_PATH, BASE_PATH))
    local('sed -i -e \'s/\/media\//https:\/\/snipt.s3.amazonaws.com\//g\' %s/media/css/style.css' % BASE_PATH)
    local('rm %s/media/css/style.css-e' % BASE_PATH)
    local('cat %s/media/css/*.css > %s/media/cache/snipt.css' % (BASE_PATH, BASE_PATH))
    local('cat %s/media/js/libs/*.js %s/media/js/plugins/*.js %s/media/js/src/*.js %s/media/js/src/modules/*.js > %s/media/cache/snipt.js' % (BASE_PATH, BASE_PATH, BASE_PATH, BASE_PATH, BASE_PATH))
    local('/Users/Nick/.virtualenvs/snipt/bin/python %s/manage.py collectstatic --ignore grappelli --ignore admin --noinput' % BASE_PATH)

def deployapp(m):
    try:
        local('hg commit -m \'%s\'' % m)
    except:
        pass
    try:
        local('git add .')
        local('git commit -m \'%s\'' % m)
    except:
        pass
    local('hg push')
    local('git push -f heroku')

def deploy(m):
    staticfiles()
    deployapp(m)

def deployall(m):
    deploy(m)
    local('heroku run bin/python snipt/manage.py syncdb')
    local('heroku run bin/python snipt/manage.py migrate')