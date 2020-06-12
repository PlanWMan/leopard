# from app import apps
# from app.qichamao.views import qcmbaseinfo, qcmsearchitem, qcmsearchother
# from app.maimai.views import maimai_people_list, maimai_people_info
# from app.b2b.views import b2b_info
# from app.sq.views import sq_info
# from app.huangye.views import huangye_info
# from app.xizhi.views import xizhi_info
# from app.zhaodao88.views import zhaodao_info
from aaa.hc360.views import Hc360
from aaa import apps
# from flask import Flask
# apps = Flask(__name__)
# from flask import Flask
# apps = Flask(__name__)
# 添加启查猫的路由
# def create_qcm():
#     apps.add_url_rule('/qcm/get_base_info/', view_func=qcmbaseinfo)
#     apps.add_url_rule('/qcm/get_item/', view_func=qcmsearchitem, methods=["POST"])
#     apps.add_url_rule('/qcm/get_other/', view_func=qcmsearchother, methods=["POST"])
#
#
# # 添加脉脉的路由
# def create_maimai():
#     apps.add_url_rule('/mm/get_plist/', view_func=maimai_people_list, methods=["POST"])
#     apps.add_url_rule('/mm/get_pinfo/', view_func=maimai_people_info, methods=["POST"])
#
#
# # 添加爱采购的路由
# def create_b2b():
#     apps.add_url_rule('/b2b/get_info/', view_func=b2b_info, methods=["POST"])
#
#
# # 添加顺企网的路由
# def create_sq():
#     apps.add_url_rule('/sq/get_info/', view_func=sq_info, methods=["POST"])
#
#
# # 添加中国黄页的路由
# def create_huangye():
#     apps.add_url_rule('/huangye/get_info/', view_func=huangye_info, methods=["POST"])


# 添加慧聪网路由
def create_hc():
    apps.add_url_rule('/hc360/get_info/', view_func=Hc360().get_resp(), methods=["POST"])


# def create_xizhi():
#     apps.add_url_rule('/xizhi/get_info/', view_func=xizhi_info, methods=["POST"])
#
#
# def create_zhaodao():
#     apps.add_url_rule('/zhaodao/get_info/', view_func=zhaodao_info, methods=["POST"])
