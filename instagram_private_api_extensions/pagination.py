import time


def page(fn, args, cursor_key='max_id', get_cursor=lambda r: r.get('next_max_id'), wait=5):
    """
    A helper method to page through a feed/listing api call

    .. code-block:: python

        from instagram_private_api import Client
        from instagram_private_api_extensions.pagination import page

        api = Client('username', 'password')
        items = []
        for results in page(api.user_feed, args={'user_id': '2958144170'}):
            if results.get('items'):
                items.extend(results['items'])
        print(len(items))

    :param fn: function call
    :param args: dict of arguments to pass to fn
    :param cursor_key: param name for the cursor, e.g. 'max_id'
    :param get_cursor: anonymous funtion to etract the next cursor value
    :param wait: interval in seconds to sleep between api calls
    :return:
    """
    results = fn(**args)
    yield results

    cursor = get_cursor(results)
    while cursor:
        if wait:
            time.sleep(wait)
        args[cursor_key] = cursor
        results = fn(**args)
        yield results
        cursor = get_cursor(results)
