import asyncio

log = lambda msg: print(f"[queue_service]: {msg}")

# Our in-memory FIFO queue.
message_queue = asyncio.Queue()

async def handle_producer(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    log("Producer connected.")
    while True:
        line = await reader.readline()
        if not line:
            break
        decoded_line = line.decode().rstrip("\n")
        if decoded_line == "EOF":
            await message_queue.put("EOF")
            continue
        await message_queue.put(decoded_line + "\n")
    writer.close()
    await writer.wait_closed()
    log("Producer disconnected.")

async def handle_consumer(writer: asyncio.StreamWriter):
    log("Consumer connected.")
    while True:
        message = await message_queue.get()
        if message.rstrip("\n") == "EOF":
            writer.write("EOF\n".encode())
            await writer.drain()
            continue
        writer.write(message.encode())
        await writer.drain()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        role_line = await reader.readline()
        role = role_line.decode().strip()
        if role == "PRODUCER":
            await handle_producer(reader, writer)
        elif role == "CONSUMER":
            await handle_consumer(writer)
        else:
            log("Unknown client role. Closing connection.")
            writer.close()
            await writer.wait_closed()
    except Exception as e:
        log(f"Exception in handle_client: {e}")

async def run_queue_service():
    host = "127.0.0.1"
    port = 8888
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    log(f"Queue service running on {addr}")
    async with server:
        await server.serve_forever()

def main():
    try:
        asyncio.run(run_queue_service())
    except KeyboardInterrupt:
        log("Queue service stopped.")

if __name__ == '__main__':
    main()
