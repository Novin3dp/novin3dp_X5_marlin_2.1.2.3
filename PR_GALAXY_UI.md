### Description

This PR adds **Galaxy UI** (`NOVIN3DP_GALAXY_UI`), an alternative touch interface for `TFT_COLOR_UI` on 480x320 displays. It was developed and tested on an MKS Robin Nano V3 with an MKS TS35 V2.0.

The UI replaces the Color UI screens with a dark-blue "galaxy" theme:

- **Home screen:** Print / Prepare / Settings tiles, with a footer showing nozzle, bed and fan.
- **Print status screen:** G-code thumbnail, progress, elapsed and remaining time (`M73` or estimated), and Tune / Pause / Stop.
- **Print complete screen:** thumbnail, print time, height and total prints, plus Reprint / Home.
- **Storage:** a USB / SD selector, then a file grid with **QOI thumbnails** decoded while streaming from the media. No extra RAM buffer is used.
- **Motion:** a move screen with a round XY jog pad, Z and E buttons, and selectable step sizes.
- **Nozzle, bed and fan:** dedicated screens with a slider, presets and cooldown.
- **Other screens:** Settings, Leveling / Mesh, Z-offset, Filament and About.
- **Marlin menus:** all of Marlin's list menus, edit screens and confirm screens are drawn in the same style. Every existing menu stays available.

All icons are 1-bit, generated at build time from a small set of sizes. The three home icons are 8-bit palette images from [Microsoft Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (MIT, license included in `lcd/tft/galaxy`). The background is computed per pixel row, so it uses no image flash.

Slicer setup: export thumbnails as `48x48/QOI, 150x150/QOI` (e.g., in OrcaSlicer, *G-code thumbnails*).

#### Core changes
These changes are only active when `NOVIN3DP_GALAXY_UI` is enabled.

- **`canvas` / `tft_queue`:** new canvas items for the computed background, rounded semi-transparent panels, 1-bit bitmaps and custom draw callbacks. Each text item stores its font, and glyph edges are antialiased against what is underneath.
- **`touch`:** two new control types, `GX_ACTION` (with optional auto-repeat) and `GX_SLIDER`. `MAX_CONTROLS` is raised to 40.
- **`buzzer`:** a new `is_active()`.
  - On the TS35 the beeper current disturbs the display ribbon, so drawing pauses while a tone is playing.
  - Without this, screen corruption was visible on every touch beep.
- **`marlinui`:**
  - The status screen no longer opens the Marlin main menu on a stray click, because the UI has its own buttons.
  - A full redraw after leaving a menu is not deferred by the planner throttle. Without this, the screen stayed blank for several seconds while printing.
- **`ui_480x320.h`:** the Galaxy UI uses the compact 14px NotoSans layout.

#### Other additions
- **`TFT_SPI1_PRESCALER`:** an optional override of the STM32 TFT SPI1 clock. The default is unchanged.
  - On the Robin Nano V3 the TS35 is on SPI1 (84 MHz bus), so the default `_4` gives 21 MHz.
  - `_2` (42 MHz) was stable in testing and roughly halves screen draw time.
- **CI test:** `buildroot/tests/mks_robin_nano_v3` builds the Galaxy UI with an MKS TS35.

### Requirements

- A 480x320 TFT with touch, using `TFT_COLOR_UI` + `NOVIN3DP_GALAXY_UI`.
- Tested on: MKS Robin Nano V3 (STM32F407) + MKS TS35 V2.0, with USB flash drive and onboard SD.

### Benefits

- A modern, touch-first UI for the many 480x320 TFT printers.
- G-code thumbnails on the file list and the print screen.
- Faster access to common actions (move, temperatures, fan, files) without losing any Marlin menu.

### Configurations

Enable in `Configuration.h`:
```cpp
#define MKS_TS35_V2_0            // or another 480x320 touch TFT
#define TFT_COLOR_UI
#define NOVIN3DP_GALAXY_UI
#define GALAXY_TOUCH_BEEP        // optional
```

### Screenshots

<!-- Drag the photos here, one per line, with a caption -->
- Home screen:
- Print status (thumbnail, times):
- Print complete:
- Storage selector (USB / SD):
- File grid with thumbnails:
- File details:
- Move (XY jog pad):
- Nozzle / bed / fan slider:
- Settings:
- Marlin list menu in Galaxy style:

### Notes for reviewers

- **Hard-coded text:** the UI strings are currently English literals. I can move them to `MSG_` language strings if the feature is accepted in principle.
- **Naming:** I'm open to renaming the option, e.g. to a more generic `TFT_GALAXY_UI`.

### Related Issues

None.
