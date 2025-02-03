# CheshireCat Python SDK

----

**CheshireCat Python SDK** is a library to help the implementation
of [Cheshire Cat](https://github.com/matteocacciola/cheshirecat-core) on a Python Project

* [Installation](#installation)
* [Usage](#usage)

## Installation

To install CheshireCat Python SDK, run:

```bash
pip install cheshirecat-python-sdk
```

## Usage
Initialization and usage:

```python
from cheshirecat_python_sdk import CheshireCatClient, Configuration

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)

cheshire_cat_client = CheshireCatClient(configuration)
```
Send a message to the websocket:

```python
from cheshirecat_python_sdk import Message

notification_closure = lambda message: pass # handle websocket notification, like chat token stream

# result is the result of the message
result = cheshire_cat_client.message().send_websocket_message(
    Message("Hello world!", 'user', []),  # message body
    notification_closure # websocket notification closure handle
)
```

Load data to the rabbit hole:
```python
import asyncio

# file
result = asyncio.run(cheshire_cat_client.rabbit_hole().post_file(file, None, None))

# url
result = asyncio.run(cheshire_cat_client.rabbit_hole().post_web(url, None, None))
```

Memory management utilities:

```python
from cheshirecat_python_sdk import Collection

cheshire_cat_client.memory().get_memory_collections()  # get number of vectors in the working memory
cheshire_cat_client.memory().get_memory_recall("HELLO")  # recall memories by text

# delete memory points by metadata, like this example delete by source
cheshire_cat_client.memory().delete_memory_points_by_metadata(Collection.Declarative, {"source": url})
```
