import socket
import ssl
import re
from html.parser import HTMLParser

class CrawlerHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.flag = None
        self.recordingflag = False

    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
            for (property, value) in attrs:
                if property == "href":
                    self.links.append(value)
        if (tag == "h3"):
            for (property, value) in attrs:
                if (property == 'class' and value == "secret_flag"):
                    self.recordingflag = True
    def handle_endtag(self, tag):
        if (tag == "h3"):
            self.recordingflag = False

    def handle_data(self, data):
        if (self.recordingflag):
            print(data)
        if (re.search("FLAG",data)):
            print(data)

            


class HttpCrawler:
    def __init__(self, server, port, cookie):
        self.server = server
        self.port = port
        self.socket = None
        self.ssl_context = None
        self.cookie = cookie

    def getRequest(self, url):
        cookies = "; ".join([f"{k}={v}" for k, v in self.cookie.items()])
        page_request = f"GET {url} HTTP/1.1\r\nHost: {self.server}\r\nUser-Agent: Crawler/1.0\r\nCookie: {cookies}\r\nConnection: Keep-Alive\r\nContent-Length: 0\r\n\r\n"
        return page_request

    def getPage(self, url):
        if (not self.socket or self.ssl_context):
            new_socket = socket.create_connection((self.server, self.port))
            self.ssl_context = ssl.create_default_context()
            self.socket = self.ssl_context.wrap_socket(new_socket, server_hostname=self.server)
        self.socket.sendall(self.getRequest(url).encode('ascii'))

        response_data = ""
        content_length = float("inf")
        data_received = 0
        response_code = 0
        while data_received < content_length:
            data = self.socket.recv()
            data_received += len(data)

            
            if not data:
                break
            response_data += data.decode("ascii")
            if content_length == float("inf"):
                matched = re.search(r'content-length: [0-9]+\r\n',response_data)
                if matched:
                    size_header = matched.group(0)
                    content_length = int(size_header.split(":")[1].strip())
            if response_code == 0:
                matched = re.search(r'HTTP/1.1 [0-9]+ ',response_data)
                response_code = int(matched.group(0).split(" ")[1])

        if (response_code == 302):
            matched = re.search(r'location: .+\r\n', response_data)
            return [matched.group(0).split(":")[1].strip()], response_code
        parser = CrawlerHTMLParser()
        parser.feed(response_data)
        return parser.links, response_code
    def crawl(self):
        visited = set()
        visited.add("/")
        visited.add("/accounts/logout")
        stack  = ["/fakebook/"]
        while (len(stack) > 0):
            nextlink = stack.pop()
            if (nextlink[0] != "/"):
                print(nextlink)
            if nextlink not in visited:
                # print("Crawling: ", nextlink)
                
                links, response_code = self.getPage(nextlink)
                if (response_code == 503):
                    stack.append(nextlink)
                    continue
                for link in links:
                    stack.append(link)
                visited.add(nextlink)
        self.socket.close()
        

        
        


    