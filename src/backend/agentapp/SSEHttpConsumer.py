# core/consumers.py
import json
import asyncio
from channels.generic.http import AsyncHttpConsumer
from channels.layers import get_channel_layer
from urllib.parse import parse_qs


class SSEHttpConsumer(AsyncHttpConsumer):
    """
    SSE Consumer
    """

    async def handle(self, body):
        # parse query string and get all query parameters
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        session_id = query_params.get("session_id", [None])[0]


        if not session_id:
            # return http 401 error
            self.send_response(404, f"Session ID not found")
            return
        
        # response headers
        headers = [
            (b"content-type", b"text/event-stream"),
            (b"cache-control", b"no-cache"),
            (b"connection", b"keep-alive"),
            (b"x-accel-buffering", b"no"),
        ]
        await self.send_headers(headers=headers)
        await self.send_body(b": connected\n\n", more_body=True)

        self.group_name = f"stream_{session_id}"

        self.channel_layer = get_channel_layer()
        self.channel_name_sse = await self.channel_layer.new_channel()

        # create a new group
        
        await self.channel_layer.group_add(self.group_name, self.channel_name_sse)

        # heartbeat task
        self.hb_task = asyncio.create_task(self.heartbeat())

        # receive messages from the group
        try:
            while True:
                msg = await self.channel_layer.receive(self.channel_name_sse)
                if msg.get("type") == "stream.message":
                    await self.send_sse_message(msg.get("message", {}), event=msg.get("event", "message"))
        except asyncio.CancelledError:
            pass

    async def disconnect(self):
        # clean up
        if hasattr(self, "hb_task"):
            self.hb_task.cancel()
        if hasattr(self, "channel_layer") and hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name_sse)

    async def send_sse_message(self, data, event="message"):
        payload = f"event: {event}\ndata: {data}\n\n".encode("utf-8")
        await self.send_body(payload, more_body=True)

    async def heartbeat(self):
        try:
            while True:
                await asyncio.sleep(15)
                await self.send_body(b"event: ping\ndata: {}\n\n", more_body=True)
        except asyncio.CancelledError:
            pass
