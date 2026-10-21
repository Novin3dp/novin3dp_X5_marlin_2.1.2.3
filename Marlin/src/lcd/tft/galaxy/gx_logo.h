/**
 * Marlin 3D Printer Firmware
 * Copyright (c) 2026 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Galaxy UI - NOVIN3DP word mark (4-bit alpha masks, run-length coded like the icons)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */
#pragma once

#include <stdint.h>

typedef struct {
  uint16_t width, height;
  const uint8_t *rle;       // 0x00-0x7F = n+1 transparent pixels, 0x80|a<<3|(n-1) = n pixels of alpha a
} gx_mask_t;

extern const gx_mask_t gx_novin_boot, gx_novin_small;
extern const uint16_t gx_novin_boot_stage[4];   // Right edge of "novin", "novin3", "novin3d", "novin3dp"

// Draw a mask tinted with a light-to-color gradient; only columns below clip_w are drawn
void gx_mask(const int16_t x, const int16_t y, const gx_mask_t &m, const uint16_t color, const uint16_t clip_w=0xFFFF);
