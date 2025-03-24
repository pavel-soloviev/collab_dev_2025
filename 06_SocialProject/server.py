import asyncio
import cowsay
import shlex

clients = {}
cow_names = set(cowsay.list_cows())

async def chat(reader, writer):
    cow_name = None
    send_task = asyncio.create_task(reader.readline())
    receive_task = None

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send_task] + ([receive_task] if receive_task else []),
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in done:
            if task is send_task:
                line = task.result().decode().strip()
                send_task = asyncio.create_task(reader.readline())
                
                if not line:
                    continue
                
                parts = shlex.split(line)
                command = parts[0]
                
                match command:
                    case "who":
                        answer = "Registered cows: " + ", ".join(clients.keys())
                    case "cows":
                        answer = "Available cows: " + ", ".join(cow_names - clients.keys())
                    case "login" if len(parts) > 1:
                        name = parts[1]
                        if name in clients:
                            answer = f"Cow {name} is already taken."
                        elif name not in cow_names:
                            answer = f"{name} is not a valid cow name."
                        else:
                            cow_name = name
                            clients[cow_name] = asyncio.Queue()
                            answer = f"You are {cow_name}. Congrats!"
                            receive_task = asyncio.create_task(clients[cow_name].get())
                    case "say" if len(parts) > 2 and cow_name:
                        target = parts[1]
                        message = " ".join(parts[2:])
                        if target in clients:
                            await clients[target].put(cowsay.cowsay(message, cow=cow_name))
                            answer = "Message sent."
                        else:
                            answer = f"Cow {target} not found."
                    case "yield" if len(parts) > 1 and cow_name:
                        message = " ".join(parts[1:])
                        for q in clients.values():
                            if q is not clients[cow_name]:
                                await q.put(cowsay.cowsay(message, cow=cow_name))
                        answer = "Message broadcasted."
                    case "quit" if cow_name:
                        del clients[cow_name]
                        cow_name = None
                        answer = "You have quit."
                    case _:
                        answer = "Invalid command or login first."
                
                writer.write(answer.encode() + b"\n")
                await writer.drain()
            
            elif task is receive_task:
                receive_task = asyncio.create_task(clients[cow_name].get())
                writer.write(task.result().encode() + b"\n")
                await writer.drain()
    
    if cow_name:
        del clients[cow_name]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
