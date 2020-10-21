import xadmin
from xadmin import views


class GlobalSettings(object):
    site_title = '易学网后台管理系统'
    site_footer = '易学网'

xadmin.site.register(views.CommAdminView, GlobalSettings)