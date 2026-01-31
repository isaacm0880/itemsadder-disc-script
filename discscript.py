#!/usr/bin/env python3
import os
import json
import yaml
import re

RESERVED_NAMESPACES = {"minecraft", "itemsadder", "ia", "default"}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def sanitize(value):
    return value.strip().lower().replace(" ", "_")

def valid_name(value):
    return re.fullmatch(r"[a-z0-9_]+", value) is not None

def touch(path):
    if not os.path.exists(path):
        with open(path, "wb"):
            pass

print("=*= itemsadder custom music disc maker")

base_path = os.getcwd()
contents_path = os.path.join(base_path, "contents")

if not os.path.exists(contents_path):
    ensure_dir(contents_path)
    print(f"Created base folder: {contents_path}")

while True:
    namespace = sanitize(input("Enter namespace for the pack (e.g, iamusic): "))
    if not namespace:
        print("Namespace cannot be empty")
        continue
    if not valid_name(namespace):
        print("Namespace must be lowercase and contain only letters, numbers, and underscores")
        continue
    if namespace in RESERVED_NAMESPACES:
        print(f"Namespace '{namespace}' is reserved and cannot be used")
        continue
    break

pack_path = os.path.join(contents_path, namespace)

configs = os.path.join(pack_path, "configs")
dicts = os.path.join(configs, "dictionaries")
resourcepack = os.path.join(pack_path, "resourcepack", namespace)

items_yml = os.path.join(configs, "items.yml")
categories_yml = os.path.join(configs, "categories.yml")
dict_yml = os.path.join(dicts, "en.yml")
sounds_json = os.path.join(resourcepack, "sounds.json")

sounds_dir = os.path.join(resourcepack, "sounds", "music_disc")
textures_dir = os.path.join(resourcepack, "textures", "item")

if os.path.exists(pack_path):
    print(f"Existing pack found in namespace '{namespace}'. New discs will be added, existing discs wont be overwritten")
else:
    print(f"Creating a pack in namespace '{namespace}'")

for p in [configs, dicts, sounds_dir, textures_dir]:
    ensure_dir(p)

for f in [items_yml, categories_yml, dict_yml, sounds_json]:
    touch(f)

print("\nYou can create multiple discs, just type 'done' when you your finished\n")

items = {}
dictionary = {}
sounds = {}
categories = {
    "info": {"namespace": namespace},
    "categories": {
        "musicdiscs": {
            "enabled": True,
            "icon": None,
            "name": "Music Discs",
            "items": []
        }
    }
}

disc_counter = 1
created_any = False

while True:
    print(f"=*= Disc {disc_counter}")

    raw = input("Enter disc name: ").strip()
    if raw.lower() == "done":
        break

    name = sanitize(raw)
    if not name:
        print("Disc name cant be empty")
        continue
    if not valid_name(name):
        print("Disc name must be lowercase and contain only letters, numbers, and underscores")
        continue

    description = input("Enter disc description: ").strip()
    if not description:
        print("Disc description cant be empty")
        continue

    disc_id = f"music_disc_{name}"
    sound_key = f"music_disc.{name}"

    ogg_path = os.path.join(sounds_dir, f"{name}.ogg")
    png_path = os.path.join(textures_dir, f"{disc_id}.png")
    touch(ogg_path)
    touch(png_path)

    dictionary[f"display-name-{disc_id}"] = description

    sounds[sound_key] = {
        "sounds": [f"{namespace}:music_disc/{name}"]
    }

    items[disc_id] = {
        "enabled": True,
        "display_name": f"display-name-{disc_id}",
        "permission": f"{namespace}.{disc_id}",
        "resource": {
            "material": "STICK",
            "generate": True,
            "textures": [f"item/{disc_id}"]
        },
        "behaviours": {
            "music_disc": {
                "song": {
                    "name": f"{namespace}:{sound_key}",
                    "description": description
                }
            }
        }
    }

    categories["categories"]["musicdiscs"]["items"].append(f"{namespace}:{disc_id}")

    print(f"\nDisc '{disc_id}' ready. Place your .ogg and .png files in:")
    print(ogg_path)
    print(png_path)
    print("Blank placeholder files were created for you.\n")

    created_any = True
    disc_counter += 1

if created_any:
    with open(items_yml, "w") as f:
        yaml.dump({"info": {"namespace": namespace}, "items": items}, f, sort_keys=False)

    with open(dict_yml, "w") as f:
        yaml.dump(
            {"info": {"namespace": namespace, "dictionary-lang": "en"}, "dictionary": dictionary},
            f,
            sort_keys=False
        )

    with open(categories_yml, "w") as f:
        yaml.dump(categories, f, sort_keys=False)

    with open(sounds_json, "w") as f:
        json.dump(sounds, f, indent=2)

print("Done. Replace placeholders with your actual .ogg and .png files, optionally change the dictionary settings if youd like.")
print("If this is all you needed, you can close this window now.")
