# -*- coding: UTF-8 -*- 
__author__ = "rody800"

from futures import ThreadPoolExecutor                        
from functools import partial, wraps                                     
import time                                                                                                                                      
import tornado.ioloop                                                    
import tornado.web                                                       

''' 本例子通过http get 请求异步读取服务器上一个文件
    实现对其他http请求不影响                                                                         
'''

                                                                    
tpexe = ThreadPoolExecutor(max_workers=2)                             
                                                                                                                                                                                                           
class IndexHandler(tornado.web.RequestHandler):                                                                                                
    def get(self):                                                       
        self.write("This is index page")                      
                                                                      
class FileHandler(tornado.web.RequestHandler):                                                                                             
    @tornado.web.asynchronous                                            
    def get(self, filename):                                                                                                                                                                                                                                       
        tpexe.submit( partial(self.readfile, filename)).add_done_callback(lambda future: tornado.ioloop.IOLoop.instance().add_callback(partial(self.callback_func, future)))                              
    
    def callback_func(self,future):                                            
        self.write(future.result())                                  
        self.finish()    
                                                                                 
    def readfile(self, flname):
        #模拟读文件花很长时间，time.sleep()，阻塞                                                   
        time.sleep(float(10))
        data=None
        with open(flname,"r") as fl:
           data= fl.read()                                       
        return data             
                                                                         
                                                                         
application = tornado.web.Application([                                  
    (r"/", IndexHandler),                                                                                   
    (r"/read/(.*)", FileHandler),                          
])                                                                       
                                                                         
                                                                         
if __name__ == "__main__":                                               
    application.listen(8080)                                             
    tornado.ioloop.IOLoop.instance().start()                             