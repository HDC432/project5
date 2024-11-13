# README #

## Overall Strategy ##

The code involves two major components, the HTTPS login module and the web crawler

### HTTPS Login ###

The program first tries to get the CSRF token from the website by sending a POST login request with the close on end connection. Once a response is received, we try to extract the cookie from the set-cookie header. If here is no cookie, an error will be thrown. Once the cookie is received, the connection is closed and the cookie is stored

### Web Crawler ###

The web crawler uses the cookie received for all future requests. This uses a persistent connection to speed up the subsequent requests. It uses a DFS algorithm with an explored stack to prevent loops. The home page for fakebook is added to the frontier to begin with. As long as the frontier is not empty, links are popped from it and a get request is sent. In case of a non error, the links are scraped from the response using an HTML parser and added to the frontier. In case of a redirection error, the location value is added to the frontier. In case of a 404 error, nothing happens, and in case of a server error the links is tried again.
The explored set prevents loops from being explored indefinitely. For each page, the HTML parser also checks if the flag is present, if the flag is present it is printed to the console. 

## Testing Strategy ##

In the initial phase we used print statements to make sure the cookie was being set correctly and the server was responding to the requests as expected. We also used print statements to see how the pages were being explored and whether it was handling the error cases as expected.

## Challenges faced ##

One of the challenges was to prevent the web crawler from logging itself out by accidentally by accessing the log out pages, so that was hard coded into the explored set. This was difficult to discover as the web crawler explored web pages at a very high rate. We figuired this out by observing that the web crawler was receiving logged out links towards the end, which were preceded by the visit to the logout page.