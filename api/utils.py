def chunks(data: str, size=16):
    for i in range(0, len(data), size):
        yield data[i: i + size]
