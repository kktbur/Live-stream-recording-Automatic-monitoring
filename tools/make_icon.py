from pathlib import Path

from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "assets" / "reco-box-icon.png"
FINAL_PNG = PROJECT_ROOT / "assets" / "reco-box-icon-final.png"
TARGET = PROJECT_ROOT / "assets" / "reco-box.ico"
PREVIEW = PROJECT_ROOT / "assets" / "reco-box-icon-preview.png"
SIZES = (16, 24, 32, 48, 64, 128, 256)


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    inset = max(2, round(image.width * 0.012))
    radius = round(image.width * 0.19)
    draw.rounded_rectangle(
        (inset, inset, image.width - inset - 1, image.height - inset - 1),
        radius=radius,
        fill=255,
    )
    image.putalpha(mask)
    image.save(FINAL_PNG, format="PNG")
    preview = Image.new("RGBA", image.size, "#D8DADF")
    preview.alpha_composite(image)
    preview.convert("RGB").save(PREVIEW, format="PNG")
    image.save(TARGET, format="ICO", sizes=[(size, size) for size in SIZES])
    print(f"created {FINAL_PNG}, {PREVIEW}, and {TARGET}")


if __name__ == "__main__":
    main()
