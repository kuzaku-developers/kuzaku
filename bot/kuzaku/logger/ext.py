async def printer (queue: list):
    if len (queue) != 0:
        el = queue [0]

        if isinstance (el, str):
            print (el)

            queue.pop (0)

        elif isinstance (el, dict):
            if len (el ['queue']) == 0 and el ['finished']:
                queue.pop (0)

            else:
                await printer (el ['queue'])

        else:
            raise TypeError (f'Queue cannot contain {type (el) !r} elements, only str and dict.')

# printer_task = loop () (printer)