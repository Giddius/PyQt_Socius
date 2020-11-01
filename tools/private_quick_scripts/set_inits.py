from glob import iglob

MAINDIR = r"D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/PyQt_Socius"
_conv_name = "pyqt_sorter_models.py"
for x in iglob(f"{MAINDIR}/**/{_conv_name}"):
    print(x)
