# Src files
import src.encrypter as encrypter
import src.randomHelper as random

# Models
import models.swap as swap
import models.shift as shift

if __name__ == "__main__":
    # Make converter
    converter = encrypter.encrypter()
    converter.directory_path = "models/"

    # Add models
    swap_m = swap.swap(swap.swapSettings.random)
    swap_m.setSwapAmount(5)
    swap_m.setRandomModule(random.randomHelper(random.randomSettings.random))
    converter.appendModel(swap_m)

    swap_m = swap.swap(swap.swapSettings.reverse)
    swap_m.setSwapAmount(3)
    converter.appendModel(swap_m)

    shift_m = shift.shift(shift.shiftSettings.printable)
    shift_m.setShiftAmount(15)
    converter.appendModel(shift_m)

    # Encrypt file
    convy = encrypter.encrypter()
    convy.appendModel(swap_m)
    convy.appendModel(shift_m)
    converter.setFileEncrypter(convy)

    # Export and import model
    converter.exportModel("export/main_model.txt")
    converter.importModel("export/main_model.txt")

    text = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # text = "Hallo ik ben daan.\nIk vind programeren opzich wel leuk.\nDaarnaast zou ik graag een goed betaalde baan " \
    #        "willen hebben waar ik het naar mijn zin heb.\nVoor nu lijkt het wel geinig.\nMaar het wordt wel cool denk "\
    #        "ik.\n"
    encrypted = converter.encrypt(text)
    decrypted = converter.decrypt(encrypted)
    print(f"Text\t : {text}\nEncrypted: {encrypted}\nDecrypted: {decrypted}\nSame\t : {text == decrypted}\n")

    print(converter)

