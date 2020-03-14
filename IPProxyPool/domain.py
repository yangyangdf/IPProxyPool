from settings import MAX_SCORE

class Proxy(object):
    def __init__(self,ip,port,protocol=-1,nick_type=-1,speed=-1,area=None,score=MAX_SCORE,disable_domains=[]):
        #ip:代理的IP地址
        self.ip = ip
        #port:代理IP的端口号
        self.port = port
        #protocol：代理ip支持的协议类型，http是0，https是1，http和https都支持是2
        self.protocol = protocol
        #nick_type:代理i的匿名程度，高匿：0，匿名：1，透明：2
        self.nick_type = nick_type
        #speed：代理ip的相应速度，单位s
        self.speed = speed
        #area：代理ip所在地区
        self.area = area
        #score：代理ip的评分，用于衡量代理的可用性
        self.score = score
        #默认分支可以通过配置文件进行配置，再进行代理可用性检查的时候
        #每遇到一次请求失败久减1分，减到0时删除
        #disable_domain：不可用域名列表，有些代理ip再某些域名下不可用，但是在其他域名下可用
        self.disable_domains = disable_domains

    #提供__str__方法，返回数据字符串
    def __str__(self):
        return str(self.__dict__)








