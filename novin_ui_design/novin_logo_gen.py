"""novin_gen.py SRC OUT_CPP PREVIEW : NOVIN3DP word mark -> 4-bit alpha masks (RLE) for the Galaxy UI"""
import sys, numpy as np
from PIL import Image
src, out, prev = sys.argv[1:4]
A = np.asarray(Image.open(src).convert('RGBA'))[..., 3].astype(np.float32)
X0, X1, Y0, Y1 = 145, 1864, 165, 328   # Bounding box of novin3dp_logo.webp
A = A[Y0:Y1 + 1, X0:X1 + 1]
glyph_end = [356, 600, 849, 913, 1156, 1377, 1620, 1864]          # n o v i n 3 d p
stages = [glyph_end[4], glyph_end[5], glyph_end[6], glyph_end[7]]  # novin, novin3, novin3d, novin3dp

def rle(px):
    o = []; i = 0
    while i < len(px):
        a = px[i]; n = 1; lim = 128 if a == 0 else 8
        while i + n < len(px) and px[i + n] == a and n < lim: n += 1
        o.append((n - 1) if a == 0 else (0x80 | (a << 3) | (n - 1))); i += n
    return o

def mask(name, width):
    h = round(A.shape[0] * width / A.shape[1])
    img = Image.fromarray(A.astype(np.uint8), 'L').resize((width, h), Image.LANCZOS)
    a4 = np.clip(np.round(np.asarray(img).astype(np.float32) * 15 / 255), 0, 15).astype(int)
    data = rle(a4.flatten().tolist())
    cuts = [round((e - X0 + 1) * width / A.shape[1]) for e in stages]
    code = f"// {name}: {width}x{h}, 4-bit alpha, {len(data)} bytes RLE\n"
    code += f"static const uint8_t {name}_rle[{len(data)}] = {{\n"
    for j in range(0, len(data), 32): code += '  ' + ','.join('0x%02x' % x for x in data[j:j + 32]) + ',\n'
    code += f"}};\nconst gx_mask_t {name} = {{ {width}, {h}, {name}_rle }};\n"
    code += f"const uint16_t {name}_stage[4] = {{ {', '.join(str(c) for c in cuts)} }};   // novin | 3 | d | p\n\n"
    return code, a4, cuts

c1, b1, k1 = mask('gx_novin_boot', 440)
c2, b2, k2 = mask('gx_novin_small', 220)
hdr = """/**
 * Marlin 3D Printer Firmware
 * Copyright (c) 2026 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * NOVIN3DP word mark for the Galaxy UI (generated): 4-bit alpha masks, run-length coded
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

#include "../../../inc/MarlinConfigPre.h"

#if ENABLED(NOVIN3DP_GALAXY_UI)

#include "gx_logo.h"

"""
open(out, 'w', newline='\n').write(hdr + c1 + c2 + "#endif // NOVIN3DP_GALAXY_UI\n")

# Preview: the four boot stages and the small logo on the dark background, white tint with gradient
H = 4 * (b1.shape[0] + 16) + b2.shape[0] + 40
bg = np.zeros((H, 480, 3), np.float32); bg[:] = (4, 9, 24)
def put(a4, ox, oy, clip):
    h, w = a4.shape
    for r in range(h):
        k = (h - 1 - r) * 90 / h / 255
        col = np.array([226, 246, 255]) + (255 - np.array([226, 246, 255])) * k
        al = (a4[r, :clip] * 17 / 255.0)[:, None]
        bg[oy + r, ox:ox + clip] = bg[oy + r, ox:ox + clip] * (1 - al) + col * al
y = 10
for cut in k1:
    put(b1, 20, y, cut); y += b1.shape[0] + 16
put(b2, (480 - b2.shape[1]) // 2, y + 10, b2.shape[1])
Image.fromarray(bg.astype(np.uint8)).resize((960, H * 2), Image.NEAREST).save(prev)
print('boot', b1.shape, k1, 'small', b2.shape, len(c1) + len(c2))
