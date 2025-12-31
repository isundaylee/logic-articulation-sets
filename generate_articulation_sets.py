#!/usr/bin/env python3
"""
Generate Logic Pro articulation set files (.plist) based on a hardcoded mapping.

This script creates articulation set files that map MIDI notes (C1-B1) to
articulation names, following the format used by Logic Pro.
"""

import argparse
import plistlib
import shutil
import sys
import os


# Root path for articulation sets
ROOT_PATH = "output"

# Logic Pro articulation sets location
LOGIC_PRO_PATH = os.path.expanduser("~/Music/Audio Music Apps/Articulation Settings")


# Hardcoded mapping from relative paths to articulation set configurations
# Each entry maps a relative path to an articulation mapping dictionary
PATH_TO_ARTICULATION_MAPPING = {
    "Musio - CineStrings Solo/Violin I.plist": {
        24: "Legato - Performance",  # C1
        25: "Legato - Bow Change",  # C#1
        26: "Legato - Espressivo",  # D1
        27: "Sustain",  # D#1
        28: "Sustain - Espressivo",  # E1
        29: "Sustain - Infinite Bow",  # F1
        30: "Marcato",  # F#1
        31: "Staccato",  # G1
        32: "Spiccato",  # G#1
        33: "Short Spiccato",  # A1
        34: "Pizzicato",  # A#1
        35: "Tremolo",  # B1
    },
    "Musio - CineStrings Solo/Violin II.plist": {
        24: "Legato - Performance",  # C1
        25: "Legato - Bow change",  # C#1
        26: "Legato - Espressivo",  # D1
        27: "Sustain",  # D#1
        28: "Sustain - Espressivo",  # E1
        29: "Sustain - Infinite Bow",  # F1
        30: "Marcato",  # F#1
        31: "Staccato",  # G1
        32: "Spiccato",  # G#1
        33: "Short Spiccato",  # A1
        34: "Pizzicato",  # A#1
        35: "Bartok Pizzicato",  # B1
        36: "Tremolo",  # C2
    },
    "Musio - CineStrings Solo/Viola.plist": {
        24: "Legato - Performance",  # C1
        25: "Legato - Bow Change",  # C#1
        26: "Legato - Espressivo",  # D1
        27: "Sustain",  # D#1
        28: "Sustain - Espressivo",  # E1
        29: "Sustain - Infinite Bow",  # F1
        30: "Marcato",  # F#1
        31: "Staccato",  # G1
        32: "Spiccato",  # G#1
        33: "Short Spiccato",  # A1
        34: "Pizzicato",  # A#1
        35: "Bartok Pizzicato",  # B1
        36: "Tremolo",  # C2
    },
    "Musio - CineStrings Solo/Cello.plist": {
        24: "Legato - Performance",  # C1
        25: "Legato - Bow Change",  # C#1
        26: "Legato - Espressivo",  # D1
        27: "Sustain",  # D#1
        28: "Sustain - Espressivo",  # E1
        29: "Sustain - Infinite Bow",  # F1
        30: "Marcato",  # F#1
        31: "Staccato",  # G1
        32: "Spiccato",  # G#1
        33: "Pizzicato",  # A1
    },
    "Musio - CineStrings Solo/Bass.plist": {
        72: "Legato - Performance",  # C5
        73: "Legato - Bow Change",  # C#5
        74: "Legato - Espressivo",  # D5
        75: "Sustain",  # D#5
        76: "Sustain - Espressivo",  # E5
        77: "Sustain - Infinite Bow",  # F5
        78: "Marcato",  # F#5
        79: "Staccato",  # G5
        80: "Spiccato",  # G#5
        81: "Pizzicato",  # A5
        82: "Bartok Pizzicato",  # A#5
    },
    "Spitfire - Chamber Strings Essentials.plist": {
        0: "Legato",
        1: "Long",
        2: "Spiccato",
        3: "Staccato",
        4: "Pizzicato",
        5: "Long Harmonics",
        6: "Tremolo",
        7: "Trill Minor 2nd",
        8: "Trill Major 2nd",
    }
}


def create_articulation_dict(articulation_id, name, mb1_value):
    """Create a single articulation dictionary entry."""
    articulation = {
        "ArticulationID": articulation_id,
        "ID": 1000 + articulation_id,
        "Name": name,
        "Output": [{"MB1": mb1_value, "Status": "Note On"}],
    }

    return articulation


def generate_articulation_set(articulation_mapping, name, output_path):
    """
    Generate a Logic Pro articulation set plist file.

    Args:
        articulation_mapping: Dictionary mapping MIDI notes to articulation names
        name: Name of the articulation set (will be used in the plist)
        output_path: Full path to save the file
    """
    # Create articulations array
    articulations = []
    articulation_id = 1

    # Sort by MIDI note number to maintain order
    for midi_note in sorted(articulation_mapping.keys()):
        articulation_name = articulation_mapping[midi_note]
        mb1_value = midi_note  # MB1 is the actual MIDI note number

        articulation = create_articulation_dict(
            articulation_id, articulation_name, mb1_value
        )
        articulations.append(articulation)
        articulation_id += 1

    # Extract filename for the Name field
    filename = os.path.basename(output_path)

    # Create the plist structure
    plist_data = {
        "Articulations": articulations,
        "InputMidiChannel": -1,
        "MultipleOutputsActive": False,
        "Name": filename,
        "OctaveOffset": 0,
        "Switches": [],
        "SwitchingEnabled": False,
    }

    # Create directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write the plist file
    with open(output_path, "wb") as f:
        plistlib.dump(plist_data, f)

    print(f"Generated articulation set: {output_path}")
    print(f"  Name: {filename}")
    print(f"  Articulations: {len(articulations)}")

    return output_path


def copy_to_logic_pro():
    """
    Copy all files and folders from output/ to the Logic Pro location.
    """
    if not os.path.exists(ROOT_PATH):
        print(f"Error: Output directory '{ROOT_PATH}' does not exist", file=sys.stderr)
        return

    # Ensure Logic Pro directory exists
    os.makedirs(LOGIC_PRO_PATH, exist_ok=True)

    # Copy each top-level item in output/
    copied_items = []
    for item in os.listdir(ROOT_PATH):
        source_path = os.path.join(ROOT_PATH, item)
        dest_path = os.path.join(LOGIC_PRO_PATH, item)

        if os.path.isdir(source_path):
            # Delete destination folder if it exists, then copy
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
            copied_items.append(f"Directory: {item}")
        else:
            # Copy file
            shutil.copy2(source_path, dest_path)
            copied_items.append(f"File: {item}")

    if copied_items:
        print(f"\nCopied to Logic Pro location ({LOGIC_PRO_PATH}):")
        for item in copied_items:
            print(f"  {item}")
    else:
        print(f"No items found in '{ROOT_PATH}' to copy")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Logic Pro articulation set files (.plist)"
    )
    parser.add_argument(
        "--copy-overwrite",
        action="store_true",
        help="Copy generated files to Logic Pro articulation settings directory",
    )
    args = parser.parse_args()

    print(f"Generating {len(PATH_TO_ARTICULATION_MAPPING)} articulation set(s)...\n")

    # Clear output directory if it exists
    if os.path.exists(ROOT_PATH):
        shutil.rmtree(ROOT_PATH)

    # Generate all articulation sets
    for path_key, articulation_mapping in sorted(PATH_TO_ARTICULATION_MAPPING.items()):
        # Build full output path
        output_path = os.path.join(ROOT_PATH, path_key)

        # Extract name from path (filename without extension)
        name = os.path.splitext(os.path.basename(path_key))[0]

        generate_articulation_set(articulation_mapping, name, output_path)

    # Copy all files from output/ to Logic Pro location if requested
    if args.copy_overwrite:
        copy_to_logic_pro()


if __name__ == "__main__":
    main()
