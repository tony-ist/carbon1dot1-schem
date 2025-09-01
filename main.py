import mcschematic

def main():    
    schem = mcschematic.MCSchematic()
    barrel = mcschematic.BlockDataDB.BARREL.fromSS(10)
    schem.setBlock((0, -1, 0), barrel)
    schem.save("schematics", "schem", mcschematic.Version.JE_1_21_5)
    

if __name__ == "__main__":
    main()
