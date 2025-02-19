import asyncio
import os

log = lambda msg: print(f"[file_writer]: {msg}")


async def file_writer(host: str, port: int):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write("CONSUMER\n".encode())
    await writer.drain()
    log("File writer started and connected.")

    while True:
        header = await reader.readline()
        if not header:
            break
        header_decoded = header.decode().rstrip("\n")
        if header_decoded.startswith("FILE:"):
            output_file = header_decoded[len("FILE:"):].strip()
            log(f"Receiving file; writing to {output_file}")
            try:
                directory = os.path.dirname(output_file)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

                with open(output_file, 'w', encoding='ascii') as f:
                    while True:
                        line = await reader.readline()
                        if not line:
                            break
                        decoded_line = line.decode()
                        log('Writing a line')
                        if decoded_line[-4:] == "EOF\n":
                            f.write(decoded_line[:-4])
                            log(f"Finished writing {output_file}")
                            break
                        f.write(decoded_line)
            except Exception as e:
                log(f"Error writing to {output_file}: {e}")
        else:
            log("Unexpected message:", header_decoded)

    writer.close()
    await writer.wait_closed()
    log("File writer finished.")


def main():
    host = "127.0.0.1"
    port = 8888
    asyncio.run(file_writer(host, port))


if __name__ == '__main__':
    main()