# doSelect
Created a Rest API using Python/Django

Created a service which exposes a RESTful API, that can be used to manage images used by other services. This service can be used to store, update, retrieve and delete images.


The image is stored on the file-system where this service lives.
To use this API, an API access key has to be generate using a management command. This access key should be used to authenticate all API calls.

Main Features of this API are:

Lossless compression of images
Support for more image types (PNG, JPEG, GIF)
Endpoint to re-generate the access key
