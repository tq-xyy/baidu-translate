import math


def sign(string, gtk):
    if len(string) > 30:
        center = math.floor(len(string) / 2)
        string = string[:10] + string[center - 5:center + 5] + string[-10:]

    [p, q] = map(int, gtk.split('.'))

    g = p

    for b in bytes(string, 'utf-8'):
        g += b
        g = (g + (g << 10)) & 0xffffffff
        g = g ^ (g >> 6)  # TODO: g = g ^ (g >>> 6)

    g = (g + (g << 3)) & 0xffffffff
    g = g ^ (g >> 11)  # TODO: g = g ^ (g >>> 6)
    g = ((g + (g << 15)) & 0xffffffff) ^ q

    if g <= 0:
        g = (0x7fffffff & g) + 0x80000000

    g = g % 1000000

    return str(g) + '.' + str(g ^ p)
