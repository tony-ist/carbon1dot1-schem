import mcschematic
import os
import sys


def binary_txt_to_carbon_v1_1_schematic(input_file: str) -> None:
    schematic = mcschematic.MCSchematic()
    barrel_ss_values = []

    with open(input_file, "r") as file:
        lines = file.readlines()

        # Process in blocks of 64 lines
        for chunk_start in range(0, len(lines), 64):
            # Get the current 64-line chunk and pad if needed
            chunk = lines[chunk_start:chunk_start + 64]
            if len(chunk) < 64:
                chunk += ['0' * 8] * (64 - len(chunk))  # Pad to ensure we have 64 lines

            # Create signal strength values for each y-stack (8 barrels) in the current chunk
            for barrel_stack in range(16):  # There are 16 barrel stacks in each chunk
                for bit_position in range(8):  # 8 nibbles per barrel stack, one for each bit
                    # Gather bits from lines 0, 16, 32, and 48 for current bit position in chunk
                    nibble_bits = [
                        chunk[barrel_stack + offset][bit_position] if barrel_stack + offset < len(chunk) else '0'
                        for offset in [0, 16, 32, 48]
                    ]
                    # Reverse nibble to make the 1st line LSB and 49th line MSB
                    nibble = ''.join(nibble_bits[::-1])

                    # Convert nibble to an integer and add to barrel_ss_values
                    barrel_ss_values.append(int(nibble, 2))

    # Now that we have the barrel signal strength values, convert it to a schematic
    # Every 8 indices (starting 0-7 ...) will be one prom line
    z_coord_offset_list = list(range(0, 63, 2))
    x_coord_offset_list = list(range(0, 511, 2))
    y_coord_offset_list = list(range(0, 15, 2))

    # Generate coord combinations in order and place the corresponding ss barrels
    coord_list = [(x, -y, z) for x in x_coord_offset_list for z in z_coord_offset_list for y in y_coord_offset_list]
    for i, ss in enumerate(barrel_ss_values):\
        # Move schematic one down so that it can be pasted by standing on the first barrel
        placement_coord = (coord_list[i][0], coord_list[i][1] - 1, coord_list[i][2])
        if ss > 0:
            schematic.setBlock(placement_coord, mcschematic.BlockDataDB.BARREL.fromSS(ss))
        else:
            schematic.setBlock(placement_coord, "white_terracotta")

    # Extract filename without extension and save with .schem
    output_file = os.path.splitext(input_file)[0]
    schematic.save("", output_file, mcschematic.Version.JE_1_21_5)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        binary_txt_to_carbon_v1_1_schematic(input_filename)
    else:
        print("Usage: uv run main.py <input_filename>")
