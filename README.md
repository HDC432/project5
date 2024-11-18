# README #

## Overall Strategy ##

This project implements a web crawler designed to interact with a simulated social networking site called Fakebook. The crawler logs into the website, retrieves session cookies, and then crawls pages.

The code involves two major components, the HTTPS login module and the web crawler.

### HTTPS Login ###

The program first tries to get the CSRF token from the website by sending a POST login request with the close on end connection. The CSRF token is embedded in a hidden field within the HTML form on the page. Once a response is received, we try to extract the cookie from the Set-Cookie header. If here is no cookie, an error will be thrown. After successfully storing the necessary cookies and CSRF token, the program constructs a POST request with the user’s username, password and CSRF token to log in. Once the login is processed, the program checks for a sessionid cookie in the response to confirm successful authentication.

### Web Crawler ###

The web crawler uses the cookie received for all future requests. This uses a persistent connection to speed up the subsequent requests. It uses a DFS algorithm with an explored stack to prevent loops. The home page for fakebook is added to the frontier to begin with. As long as the frontier is not empty, links are popped from it and a get request is sent. In case of a non error, the links are scraped from the response using an HTML parser and added to the frontier. In case of a redirection error, the location value is added to the frontier. In case of a 404 error, nothing happens, and in case of a server error the links is tried again.
The explored set prevents loops from being explored indefinitely. For each page, the HTML parser also checks if the flag is present, if the flag is present it is printed to the console. 

## Testing Strategy ##

In the initial phase we used print statements to make sure the cookie was being set correctly and the server was responding to the requests as expected. We also used print statements to see how the pages were being explored and whether it was handling the error cases as expected.

## Challenges faced ##

One of the challenges was to prevent the web crawler from logging itself out by accidentally by accessing the log out pages, so that was hard coded into the explored set. This was difficult to discover as the web crawler explored web pages at a very high rate. We figuired this out by observing that the web crawler was receiving logged out links towards the end, which were preceded by the visit to the logout page.

Another challenge faced during the implementation was retrieving the csrfmiddlewaretoken, which is stored as a hidden field in the login page's HTML form. This hidden field is critical for validating the login request, as the server uses it to ensure that the request originates from the legitimate login page and not from an unauthorized source. By inspecting the page in a browser's developer tools, csrfmiddlewaretoken can be found in the the hidden \<input\> field of the  \<form\> structure.