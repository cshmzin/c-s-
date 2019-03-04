#导入模块
import socketserver
import json
import urllib.request
import pymysql
import pymysql.cursors
from DBUtils.PooledDB import PooledDB


#连接数据库
pool=PooledDB(pymysql,2,
              host='localhost',
              user='root',
              passwd='123456',
              db='test',
              port=3306,
              charset='utf8')

db = pool.connection()
cur = db.cursor()

class MyServer(socketserver.BaseRequestHandler):
	#handle方法报错则会跳过
	def setup(self):
		pass
	
	def handle(self):
		print('有新客户端连接!!')
		#定义连续变量
		self.allname = '0'
		self.allpwd = '0'
		
		while True:
			conn = self.request
			date = conn.recv(1024)#接受客户端数据
			
			
			if date == b"denglu":   #         检验密码操作。。。。。。。。。。。。
				id = 0
				print("用户:",self.client_address,"登陆验证开始:")
				gi = 'yes'
				gj = 'no'
				gp = 'same'
				conn.sendto(gi.encode(),self.client_address)
				date = conn.recv(1024)
				zhanghao = date.decode() #获取账号
				print(zhanghao)
				conn.sendto(gi.encode(),self.client_address)
				date = conn.recv(1024)
				mima = date.decode() #获取密码
				print(mima)
				
				cur.execute("SELECT name,pwd,state FROM user")#获取数据库信息
				results = cur.fetchall()
				db.commit()
				
				for row in results: #开始验证
					Name = row[0]
					Pwd = row[1]
					State = row[2]
					if zhanghao == Name and mima == Pwd:
						if State == 0:
							id = 1
							conn.send(gi.encode())
							cur.execute("UPDATE user SET state = 1 WHERE name = '"+Name+"' AND pwd = '"+Pwd+"'")
							cur.execute("UPDATE xingxi SET state = 1 WHERE name = '"+Name+"'")
							cur.execute("UPDATE allgroup SET state = 1 WHERE name = '"+Name+"'")
							db.commit()
							self.allname = Name
							self.allpwd = Pwd
							print(self.client_address,"验证成功")
						else:
							id = 1
							conn.send(gp.encode())
				if id == 0:
					conn.send(gj.encode())
					print(self.client_address,"验证失败")
					
			if date == b"zhuce":  #            注册账号操作。。。。。。。。。。。。。。。
				print(self.client_address,"注册开始:")
				gi = 'yes'
				conn.send(gi.encode())  
				date = conn.recv(1024)
				newzhanghao = date.decode() #获取账号 
				conn.send(gi.encode())
				print(newzhanghao)
				date = conn.recv(1024) 
				newmima = date.decode() #获取密码
				conn.send(gi.encode())
				print(newmima)
				date = conn.recv(1024)
				newname = date.decode() #获取名字
				conn.send(gi.encode())
				print(newname)
				date = conn.recv(1024)
				newschool = date.decode() #获取学校
				conn.send(gi.encode())
				print(newschool)
				date = conn.recv(1024)
				newmajor = date.decode() #获取专业
				conn.send(gi.encode())
				print(newmajor)
				date = conn.recv(1024)
				newid = date.decode() #获取id
				conn.send(gi.encode())
				print(newid)
				date = conn.recv(1024)
				newclass = date.decode() #获取班级
				print(newclass)
				cur.execute("insert into user(name,pwd,state) values(%s,%s,0)",(newzhanghao,newmima))
				db.commit()
				cur.execute("insert into xingxi(sname,sid,school,class,major,name,state) values(%s,%s,%s,%s,%s,%s,0)",(newname,newid,newschool,newclass,newmajor,newzhanghao))
				db.commit()
				conn.send(gi.encode())
				print(self.client_address,"注册完成！！")
				
			if date == b"xianshi": #            显示在线用户操作。。。。。。。。。。。。。。
				gi = "yes"
				gy = "no"
				gp = "Nomore"
				print("用户",self.client_address,"请求显示")
				conn.send(gi.encode())
				date = conn.recv(1024)
				print(date.decode())
				cur.execute("SELECT sname FROM xingxi WHERE state = 1")#获取登录状态的用户
				results = cur.fetchall()
				db.commit()
				for row in results:
					Name = row[0]
					print(Name)
					conn.send(Name.encode())
					date = conn.recv(1024)
					print(date.decode())
				conn.send(gp.encode())
				print(self.client_address,"显示完毕")
				
			if date == b"allxianshi": #            显示全部用户操作。。。。。。。。。。。。。。
				gi = "yes"
				gy = "no"
				gp = "Nomore"
				print("用户",self.client_address,"请求显示")
				conn.send(gi.encode())
				date = conn.recv(1024)
				print(date.decode())
				cur.execute("SELECT sname FROM xingxi WHERE state = 1")#获取用户
				results = cur.fetchall()
				db.commit()
				for row in results:
					Name = row[0]
					print(Name)
					conn.send(Name.encode())
					date = conn.recv(1024)
					print(date.decode())
				conn.send(gp.encode())
				print(self.client_address,"显示完毕")
									
			if date == b"huoqu": #                  获取用户数据。。。。。。。。。。。。。。
				gi = "yes"
				gy = "no"
				gp = "Nomore"
				print("用户",self.client_address,"获取信息")
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				Kname = date.decode()
				print(Kname)
				
				cur.execute("SELECT sname,sid,school,class,major,name FROM xingxi WHERE  Sname = '"+Kname+"'")
				results = cur.fetchall()
				db.commit()
				
				for row in results:
					Sname = row[0]
					Sid = row[1]
					School = row[2]
					Class = row[3]
					Major = row[4]
					
				conn.send(Sname.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Sid.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(School.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Class.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Major.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(gp.encode())
				print(gp)
				
			if date == b"guanyu": #                  获取个人数据。。。。。。。。。。。。。。
				gi = "yes"
				gy = "no"
				gp = "Nomore"
				print("用户",self.client_address,"获取信息")
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				Kname = date.decode()
				print(Kname)
				
				cur.execute("SELECT sname,sid,school,class,major,name FROM xingxi WHERE  name = '"+Kname+"'")
				results = cur.fetchall()
				db.commit()
				
				for row in results:
					Sname = row[0]
					Sid = row[1]
					School = row[2]
					Class = row[3]
					Major = row[4]
					
				conn.send(Sname.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Sid.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(School.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Class.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(Major.encode())
				date = conn.recv(1024)#接受客户端数据
				print(date.decode())
				conn.send(gp.encode())
				print(gp)
			
			if date == b"fasong":#                  发送数据。。。。。。。。。。。。。。
				gi = 'yes'
				gj = 'no'
				gp = 'ok'
				hisname = '0'
				
				print('发送数据')
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				myname = date.decode()
				print(date.decode())
				
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				hisSname = date.decode().replace("space","")
				print(date.decode())
				
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				tell = date.decode()
				print(date.decode())
				
				cur.execute("SELECT name FROM xingxi WHERE  Sname = '"+hisSname+"'")
				results = cur.fetchall()
				db.commit()
				
				for row in results:
					hisname = row[0]
					
				if hisname == '0':
					print('wrong')
					
				cur.execute("insert into tell(myname,hisname,tell,who) values(%s,%s,%s,0)",(myname,hisname,tell))
				db.commit()
				
				cur.execute("insert into tell(hisname,myname,tell,who) values(%s,%s,%s,1)",(myname,hisname,tell))
				db.commit()	
					
				conn.send(gp.encode())
			
			if date == b'getmessage':#               获取聊天记录。。。。。。。。。。。。。
				gi = 'yes'
				gy = 'ok'
				gt = 'no'
				gp = 'noallmore'
				hisname = '0'
				print('获取聊天记录')
				
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				myname = date.decode()
				print(date.decode())
				conn.send(gi.encode())
				date = conn.recv(1024)#接受客户端数据
				hisSname = date.decode().replace("space","")
				print(date.decode())
				
				
				cur.execute("SELECT name FROM xingxi WHERE  Sname = '"+hisSname+"'")
				results = cur.fetchall()
				db.commit()
				
				for row in results:
					hisname = row[0]
					
				cur.execute("SELECT who,tell FROM tell WHERE  myname = '"+myname+"' and hisname = '"+hisname+"'")
				results = cur.fetchall()
				db.commit()
				
				for row in results:
					who = row[0]
					print(who)
					tell = row[1]
					print(tell)
					
					if who == 1:
						conn.send(gy.encode())
						date = conn.recv(1024)#接受客户端数据
						conn.send(tell.encode())
						date = conn.recv(1024)#接受客户端数据
					else :
						conn.send(gt.encode())
						date = conn.recv(1024)#接受客户端数据
						conn.send(tell.encode())
						date = conn.recv(1024)#接受客户端数据
				conn.send(gp.encode())
				print('获取完成')
			
			if date == b'creategroup':#             创建群聊。。。。。。。。。。。。。。。
				gi = 'yes'
				gp = 'ok'
				conn.send(gi.encode())  
				date = conn.recv(1024)
				name = date.decode() #获取账号
				conn.send(gi.encode())  
				date = conn.recv(1024)
				groupname = date.decode() #获取账号
				cur.execute("insert into allgroup(groupid,name,state) values(%s,%s,1)",(groupname,name))
				db.commit()
				conn.send(gp.encode())	
				
				
			if date == b'ingroup':#              进入群聊。。。。。。。。。。。。。。。。。。。
				groupid = '0'
				gi = 'yes'
				gp = 'ok'
				gy = 'no'
				i = 0
				conn.send(gi.encode())
				date = conn.recv(1024)
				groupname = date.decode()
				
				cur.execute("SELECT groupid FROM allgroup")#获取数据库信息
				results = cur.fetchall()
				db.commit()
				
				for row in results: #开始验证	
					groupid = row[0]
					if groupid == groupname:
						i = 1
				
				if i == 1:
					conn.send(gp.encode())
				else:
					conn.send(gy.encode())
					
			if date == b'sendgroup':#      发送群数据。。。。。。。。。。。。。。。。。。
					
				gi = 'yes'
				gj = 'no'
				gp = 'ok'
				
				print('群聊消息发送开始')
				conn.send(gi.encode())
				date = conn.recv(1024)
				name = date.decode() #获取账号
				print(name)
				conn.send(gi.encode())
				date = conn.recv(1024)
				groupname = date.decode() #获取组名
				print(groupname)
				conn.send(gp.encode())
				date = conn.recv(1024)
				tell = date.decode() #获取tell
				print(tell)
				print('结束')
				cur.execute("insert into grouptell(groupid,name,tell) values(%s,%s,%s)",(groupname,name,tell))
				db.commit()			
				conn.send(gp.encode())
				
			if date == b'showmessage': #    接受群数据。。。。。。。。。。。。。。。。。
				gi = 'yes'
				gj = 'no'
				gp = 'nomore'
				
				print('群聊消息接受开始')
				conn.send(gi.encode())
				date = conn.recv(1024)
				groupname = date.decode()
				
				cur.execute("SELECT name,tell FROM grouptell WHERE groupid = '"+groupname+"'")#获取数据库信息
				results = cur.fetchall()
				db.commit()
				
				for row in results: #开始验证
					name = row[0]
					tell = row[1]
					
					cur.execute("SELECT sname FROM xingxi WHERE  name = '"+name+"'")
					results = cur.fetchall()
					db.commit()
					
					for row in results:
						Sname = row[0]
					
					conn.send(Sname.encode())
					date = conn.recv(1024)
					conn.send(tell.encode())
					
				conn.send(gp.encode())
				
				
		
		
		
		conn.close()	
		
	
	def finish(self):
		cur.execute("UPDATE user SET state = 0 WHERE name = '"+self.allname+"' AND pwd = '"+self.allpwd+"'")
		cur.execute("UPDATE xingxi SET state = 0 WHERE name = '"+self.allname+"'")
		cur.execute("UPDATE allgroup SET state = 0 WHERE name = '"+self.allname+"'")
		db.commit()
		print("登陆结束!"+self.allname)


sk = socketserver.ThreadingTCPServer(("192.168.43.16",8888),MyServer)#创建多线程实例
sk.serve_forever()

