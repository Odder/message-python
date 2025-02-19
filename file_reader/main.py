import asyncio
import os

log = lambda msg: print(f"[file_reader]: {msg}")


async def file_reader(host: str, port: int):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write("PRODUCER\n".encode())
    await writer.drain()
    log("File reader started and connected.")

    command_file = os.path.join(os.path.dirname(__file__), "..", "command.txt")

    while True:
        if os.path.exists(command_file):
            with open(command_file, 'r', encoding='ascii') as f:
                command = f.read().strip()
            os.remove(command_file)
            if command:
                parts = command.split()
                if len(parts) != 2:
                    log("Command format invalid. Expected: <input_file> <output_file>")
                    continue
                input_file, output_file = parts
                log(f"Processing file: {input_file} -> {output_file}")
                header = f"FILE:{output_file}\n"
                writer.write(header.encode())
                await writer.drain()
                try:
                    with open(input_file, 'r', encoding='ascii') as f:
                        for line in f:
                            log('Reading a line')
                            writer.write(line.encode())
                            await writer.drain()
                except Exception as e:
                    log(f"Error reading {input_file}: {e}")
                writer.write("EOF\n".encode())
                await writer.drain()
                log(f"Finished sending {input_file}")
        else:
            await asyncio.sleep(1)

    writer.close()
    await writer.wait_closed()


def main():
    host = "127.0.0.1"
    port = 8888
    asyncio.run(file_reader(host, port))


if __name__ == '__main__':
    main()