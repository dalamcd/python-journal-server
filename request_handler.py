from journalentry.request import update_entry
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from mood import get_all_moods, get_single_mood
from journalentry import get_all_entries, get_single_entry, delete_entry, search_entries, create_entry

class HandleRequests(BaseHTTPRequestHandler):

	def _set_headers(self, status):
		self.send_response(status)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
		self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
		self.end_headers()

	def parse_url(self, path):
		
		path_params = path.split("/")

		if "?" in path_params[1]:
			tmp = path_params[1].split("?")
			resource = tmp[0]
			query = tmp[1].split("=")
			query_type = query[0]
			value = query[1]

			print(resource, query_type, value)
			return (resource, query_type, value)

		else:

			resource = path_params[1]
			id = None

			try:
				id = int(path_params[2])
			except IndexError:
				pass
			except ValueError:
				pass

			return (resource, id)

	def do_GET(self):
		self._set_headers(200)
		response = {}

		parsed_path = self.parse_url(self.path)

		if len(parsed_path) == 2:

			(resource, id) = parsed_path

			if resource == "entries":
				if id is None:
					response = f"{get_all_entries()}"
				else:
					response = f"{get_single_entry(id)}"
			elif resource == "moods":
				if id is None:
					response = f"{get_all_moods()}"
				else:
					response = f"{get_single_mood(id)}"

		elif len(parsed_path) == 3:
			
			(resource, query_type, value) = parsed_path

			if resource == "entries" and query_type == "q":
				response = f"{search_entries(value)}"
		
		self.wfile.write(response.encode())

	def do_DELETE(self):

		self._set_headers(204)
		
		(resource, id) = self.parse_url(self.path)

		if resource == "entries":
			delete_entry(id)

	def do_POST(self):
		self._set_headers(201)
		content_len = int(self.headers.get('content-length', 0))
		post_body = self.rfile.read(content_len)

		post_body = json.loads(post_body)

		(resource, id) = self.parse_url(self.path)

		new_entry = None

		if resource == "entries":
			new_entry = create_entry(post_body)

		self.wfile.write(f"{new_entry}".encode())

	def do_PUT(self):
		content_len = int(self.headers.get("content-length", 0))
		post_body = self.rfile.read(content_len)

		post_body = json.loads(post_body)

		(resource, id) = self.parse_url(self.path)

		success = False

		if resource == "entries":
			success = update_entry(post_body, id)

		if success:
			self._set_headers(201)
		else:
			self._set_headers(404)

def main():
	host = ''
	port = 8088
	HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()