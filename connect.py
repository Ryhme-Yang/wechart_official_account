# -*-coding:utf-8 -*-
import falcon
import python_repos
from falcon import uri
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,ImageReply

class Connect(object):

    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='******', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])   # 我的Token写死的，详细信息见微信开发文档
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            # 抓取科技新闻
            if msg.content=='科技' or msg.content=='科技新闻':
                reply = TextReply(content=python_repos.Content_Resp_keji(), message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
            # 抓取头条新闻
            elif msg.content=='头条' or msg.content=='头条新闻' or msg.content=='新闻':
                reply = TextReply(content=python_repos.Content_Resp_top(), message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
            # 查询天气
            elif '天气' in msg.content:
                # 查找语句中的日期标识
                index_pos = -1
                date_num = 0
                index_pos0 = msg.content.find('今日')
                if index_pos0 == -1:
                    index_pos0 = msg.content.find('今天')
                    if index_pos0 != -1:
                        index_pos = index_pos0
                        date_num = 1
                else:
                    date_num = 1
                index_pos1 = msg.content.find('明日')
                if index_pos1 == -1:
                    index_pos1 = msg.content.find('明天')
                    if index_pos1 != -1:
                        index_pos = index_pos1
                        date_num = 2
                else:
                    index_pos = index_pos1
                    date_num = 2
                index_pos2 = msg.content.find('后天')
                if index_pos2 != -1:
                    index_pos = index_pos2
                    date_num = 3
                if index_pos == -1:
                    index_pos = msg.content.find('天气')
                # 找到cityname的位置
                city_name = msg.content[:index_pos]
                if len(city_name) == 0:
                    city_name='合肥'

                rep_content = python_repos.Content_Resp_Weather(city_name,date_num)
                reply = TextReply(content=rep_content, message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
            # 爬取吾爱本周热帖
            elif msg.content=='52热帖' or msg.content=='吾爱热帖' or msg.content=='吾爱本周热帖':
                rep_content = python_repos.w2pojie_reptile_week()
                reply = TextReply(content=rep_content, message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
            
            else:
                reply = TextReply(content=msg.content, message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)
