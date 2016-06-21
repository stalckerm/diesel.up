import cookielib
import urllib
import urllib2
import re
import time
from pprint import pprint
#pprint ( vars ( poster_o ), indent = 0 )

class d_poster:
	def __init__ ( self ):
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener ( urllib2.HTTPCookieProcessor ( cj ) )
		opener.addheaders = [ ( 'User-agent', 'Mozilla Firefox' ) ]
		urllib2.install_opener ( opener )
		self.post_url='http://diesel.elcat.kg/index.php?'

		self.post_data = {
			'act':	'Post',
			'CODE': '03',
			'f': '347',
			'st': '0',
			'fast_reply_used': '1',
			'Post': ':)'
		}

		self.delete_url='http://diesel.elcat.kg/index.php?'
		self.delete_data = {
			'act':	'Mod',
			'CODE': '04',
			'f': '347',
			'st': '0',
		}

	def do_login ( self ):
		authentication_url = 'https://diesel.elcat.kg/index.php?act=Login&CODE=01'
		login_data = {
			'UserName': 'adnroid',
			'PassWord': 'unix2006'
		}
		data = urllib.urlencode ( login_data )
		req = urllib2.Request ( authentication_url, data )
		resp = urllib2.urlopen ( req )
		contents = resp.read()

		req = urllib2.Request('http://diesel.elcat.kg/index.php?showtopic=47257749')
		resp = urllib2.urlopen(req)
		contents = resp.read()
		searched_params = re.search('.*name=.?auth_key.?\svalue=.?(\w+).?\s.*',contents)
		self.auth_key = searched_params.group(1)

	def do_post ( self, topic_id ):
		post_data				= self.post_data
		post_data['auth_key']	= self.auth_key
		post_data['t']			= topic_id

		data = urllib.urlencode ( post_data )
		req = urllib2.Request ( self.post_url, data )
		resp = urllib2.urlopen ( req )
		contents = resp.read ( )

		self.__find_save_last_id ( contents, topic_id )

	def delete_last_post ( self, topic_id ):
		try:
			id_file = open ( '/tmp/diesele_id_' + topic_id, 'r' )
			self.last_id = id_file.read ( )
			id_file.close ( )

			delete_data				= self.delete_data
			delete_data['auth_key']	= self.auth_key
			delete_data['t']		= topic_id
			delete_data['p']		= self.last_id

			data = urllib.urlencode ( delete_data )
			req = urllib2.Request ( self.post_url, data )
			resp = urllib2.urlopen ( req )
		except IOError:
			print ( "Error\n" )

	def __find_save_last_id ( self, contents, topic_id ):
		self.last_id =0
		for item in re.findall ( 'entry(\d+)', contents ):
			if item > self.last_id:
				self.last_id = item
		id_file = open ( '/tmp/diesele_id_' + topic_id, 'w' )
		id_file.write ( self.last_id )
		id_file.close ( )
		return self.last_id

	def add_topic ( self, url ):
		self.__url_parser ( url )

	def __url_parser ( self, url ):
		print ( "parser\n" )
		print ( url )
		print ( "parser\n" )

		req = urllib2.Request ( url )
		resp = urllib2.urlopen ( req )
		contents = resp.read ( )
		print ( contents )


#topic_ids = ['202500814', '207102126', '194161898']
#topic_ids = ['207102126', '194161898']
#topic_ids = ['202500814']
poster_o = d_poster ( )
poster_o.do_login ( )
poster_o.add_topic ( 'http://diesel.elcat.kg/index.php?showtopic=214929049&hl=' )
#for topic_id in topic_ids:
#	poster_o.delete_last_post ( topic_id )
#	poster_o.do_post ( topic_id )
#	#time.sleep ( 100 )
exit ( 0 )

