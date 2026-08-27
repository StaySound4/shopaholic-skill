# Category Playbook: Display Monitors & Panels (`display-monitors`)

## 1. Stable Decision Physics & Panel Architectures
- **Panel Technology Fork**: OLED (infinite contrast, per-pixel dimming, potential burn-in risk) vs Mini-LED (high peak daylight HDR brightness, blooming / haloing artifacts on small subtitles) vs Fast-IPS (solid color consistency, lower static contrast).
- **Color Accuracy & Gamut**: Delta E ($\Delta E < 2$) factory calibration report on sRGB / DCI-P3 / AdobeRGB color spaces.
- **Motion Clarity & Response**: GtG (Gray-to-Gray) true transition times vs deceptive 1ms MPRT backlight strobing. Inverse ghosting overshoot.
- **Eye Care & Health**: Hardware-level low blue light vs DC dimming vs high-frequency PWM (>1920Hz flicker-free).

## 2. Mandatory Verification Registries
- **VESA DisplayHDR Registry**: `site:displayhdr.org/certified-products "{model_name}"` (Must cross-verify peak luminance and local dimming tier).
- **China Energy Efficiency (CEL)**: `site:energylabel.gov.cn "{model_number}"` (Verify standby power draw and tier).
- **TÜV Rheinland Eye Comfort**: `site:certipedia.com "{model_number}"` (Hardware low blue light verification).
