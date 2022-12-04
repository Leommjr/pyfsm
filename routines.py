""" asyncio.queue does not create new threads. It simply provides a thread-safe queue data structure that can be used to store and retrieve data in a concurrent environment.
is used to store the results of the concurrently executed coroutines. This allows the function to concurrently execute the coroutines and retrieve their results without blocking the main thread.
"""
import asyncio
async def gather(*coroutines):
    # Criação da fila para armazenar os resultados das coroutines
    # A coroutine is a special kind of function that can suspend its execution and resume it later.
    q = asyncio.Queue()

     # Adiciona as coroutines na fila
    for coroutine in coroutines:
        q.put_nowait(coroutine)

    # Executa as coroutines até que todas estejam concluídas
    while not q.empty():
        coroutine = q.get_nowait()
        try:
            # Resume a execução da coroutine
            await coroutine
        except StopIteration:
            # Remove a coroutine da fila quando ela é concluída
            q.task_done()
