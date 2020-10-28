# region [Imports]

# *NORMAL Imports -->
from enum import Enum

# *GID Imports -->
import gidlogger as glog

# *QT Imports -->

# endregion [Imports]

__updated__ = '2020-09-02 19:49:35'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Data_1]

CREATE_TABLE_STRING = 'CREATE TABLE IF NOT EXISTS "$TABLE_NAME$" ("id" INTEGER PRIMARY KEY, "item_name" TEXT NOT NULL UNIQUE, "item_description" TEXT, "item_data" INTEGER REFERENCES "$SUB_TABLE_NAME$" ("data_id"))'
CREATE_SUBTABLE_STRING = 'CREATE TABLE IF NOT EXISTS "$TABLE_NAME$" ("data_id" INTEGER PRIMARY KEY, "data_name" TEXT NOT NULL UNIQUE, "data_blob" BLOB)'
INSERT_TOC_STRING = 'INSERT OR IGNORE INTO "TOC_tbl" (table_name, table_type) VALUES ("$TABLE_NAME$", "$TABLE_TYPE$")'

QUERY_TOC_STRING = 'SELECT * FROM "TOC_tbl"'
QUERY_ALL_STRING = 'SELECT * FROM "$TABLE_NAME$"'
UPDATE_STRING = 'UPDATE "$TABLE_NAME$" SET "$COLUMN_NAME$"=? WHERE "$TARGET_COLUMN$"=?'
# endregion [Data_1]


# region [Data_2]

class Color(Enum):
    Aliceblue = (240, 248, 255, 200)
    Antiquewhite = (250, 235, 215, 200)
    Aqua = (0, 255, 255, 200)
    Aquamarine = (127, 255, 212, 200)
    Azure = (240, 255, 255, 200)
    Beige = (245, 245, 220, 200)
    Bisque = (255, 228, 196, 200)
    Black = (0, 0, 0, 200)
    Blanchedalmond = (255, 235, 205, 200)
    Blue = (0, 0, 255, 200)
    Blueviolet = (138, 43, 226, 200)
    Brown = (165, 42, 42, 200)
    Burlywood = (222, 184, 135, 200)
    Cadetblue = (95, 158, 160, 200)
    Chartreuse = (127, 255, 0, 200)
    Chocolate = (210, 105, 30, 200)
    Coral = (255, 127, 80, 200)
    Cornflowerblue = (100, 149, 237, 200)
    Cornsilk = (255, 248, 220, 200)
    Crimson = (220, 20, 60, 200)
    Cyan = (0, 255, 255, 200)
    Darkblue = (0, 0, 139, 200)
    Darkcyan = (0, 139, 139, 200)
    Darkgoldenrod = (184, 134, 11, 200)
    Darkgray = (169, 169, 169, 200)
    Darkgreen = (0, 100, 0, 200)
    Darkgrey = (169, 169, 169, 200)
    Darkkhaki = (189, 183, 107, 200)
    Darkmagenta = (139, 0, 139, 200)
    Darkolivegreen = (85, 107, 47, 200)
    Darkorange = (255, 140, 0, 200)
    Darkorchid = (153, 50, 204, 200)
    Darkred = (139, 0, 0, 200)
    Darksalmon = (233, 150, 122, 200)
    Darkseagreen = (143, 188, 143, 200)
    Darkslateblue = (72, 61, 139, 200)
    Darkslategray = (47, 79, 79, 200)
    Darkslategrey = (47, 79, 79, 200)
    Darkturquoise = (0, 206, 209, 200)
    Darkviolet = (148, 0, 211, 200)
    Deeppink = (255, 20, 147, 200)
    Deepskyblue = (0, 191, 255, 200)
    Dimgray = (105, 105, 105, 200)
    Dimgrey = (105, 105, 105, 200)
    Dodgerblue = (30, 144, 255, 200)
    Firebrick = (178, 34, 34, 200)
    Floralwhite = (255, 250, 240, 200)
    Forestgreen = (34, 139, 34, 200)
    Fuchsia = (255, 0, 255, 200)
    Gainsboro = (220, 220, 220, 200)
    Ghostwhite = (248, 248, 255, 200)
    Gold = (255, 215, 0, 200)
    Goldenrod = (218, 165, 32, 200)
    Gray = (128, 128, 128, 200)
    Green = (0, 128, 0, 200)
    Greenyellow = (173, 255, 47, 200)
    Grey = (128, 128, 128, 200)
    Honeydew = (240, 255, 240, 200)
    Hotpink = (255, 105, 180, 200)
    Indianred = (205, 92, 92, 200)
    Indigo = (75, 0, 130, 200)
    Ivory = (255, 255, 240, 200)
    Khaki = (240, 230, 140, 200)
    Lavender = (230, 230, 250, 200)
    Lavenderblush = (255, 240, 245, 200)
    Lawngreen = (124, 252, 0, 200)
    Lemonchiffon = (255, 250, 205, 200)
    Lightblue = (173, 216, 230, 200)
    Lightcoral = (240, 128, 128, 200)
    Lightcyan = (224, 255, 255, 200)
    Lightgoldenrodyellow = (250, 250, 210, 200)
    Lightgray = (211, 211, 211, 200)
    Lightgreen = (144, 238, 144, 200)
    Lightgrey = (211, 211, 211, 200)
    Lightpink = (255, 182, 193, 200)
    Lightsalmon = (255, 160, 122, 200)
    Lightseagreen = (32, 178, 170, 200)
    Lightskyblue = (135, 206, 250, 200)
    Lightslategray = (119, 136, 153, 200)
    Lightslategrey = (119, 136, 153, 200)
    Lightsteelblue = (176, 196, 222, 200)
    Lightyellow = (255, 255, 224, 200)
    Lime = (0, 255, 0, 200)
    Limegreen = (50, 205, 50, 200)
    Linen = (250, 240, 230, 200)
    Magenta = (255, 0, 255, 200)
    Maroon = (128, 0, 0, 200)
    Mediumaquamarine = (102, 205, 170, 200)
    Mediumblue = (0, 0, 205, 200)
    Mediumorchid = (186, 85, 211, 200)
    Mediumpurple = (147, 112, 219, 200)
    Mediumseagreen = (60, 179, 113, 200)
    Mediumslateblue = (123, 104, 238, 200)
    Mediumspringgreen = (0, 250, 154, 200)
    Mediumturquoise = (72, 209, 204, 200)
    Mediumvioletred = (199, 21, 133, 200)
    Midnightblue = (25, 25, 112, 200)
    Mintcream = (245, 255, 250, 200)
    Mistyrose = (255, 228, 225, 200)
    Moccasin = (255, 228, 181, 200)
    Navajowhite = (255, 222, 173, 200)
    Navy = (0, 0, 128, 200)
    Oldlace = (253, 245, 230, 200)
    Olive = (128, 128, 0, 200)
    Olivedrab = (107, 142, 35, 200)
    Orange = (255, 165, 0, 200)
    Orangered = (255, 69, 0, 200)
    Orchid = (218, 112, 214, 200)
    Palegoldenrod = (238, 232, 170, 200)
    Palegreen = (152, 251, 152, 200)
    Paleturquoise = (175, 238, 238, 200)
    Palevioletred = (219, 112, 147, 200)
    Papayawhip = (255, 239, 213, 200)
    Peachpuff = (255, 218, 185, 200)
    Peru = (205, 133, 63, 200)
    Pink = (255, 192, 203, 200)
    Plum = (221, 160, 221, 200)
    Powderblue = (176, 224, 230, 200)
    Purple = (128, 0, 128, 200)
    Red = (255, 0, 0, 200)
    Rosybrown = (188, 143, 143, 200)
    Royalblue = (65, 105, 225, 200)
    Saddlebrown = (139, 69, 19, 200)
    Salmon = (250, 128, 114, 200)
    Sandybrown = (244, 164, 96, 200)
    Seagreen = (46, 139, 87, 200)
    Seashell = (255, 245, 238, 200)
    Sienna = (160, 82, 45, 200)
    Silver = (192, 192, 192, 200)
    Skyblue = (135, 206, 235, 200)
    Slateblue = (106, 90, 205, 200)
    Slategray = (112, 128, 144, 200)
    Slategrey = (112, 128, 144, 200)
    Snow = (255, 250, 250, 200)
    Springgreen = (0, 255, 127, 200)
    Steelblue = (70, 130, 180, 200)
    Tan = (210, 180, 140, 200)
    Teal = (0, 128, 128, 200)
    Thistle = (216, 191, 216, 200)
    Tomato = (255, 99, 71, 200)
    Turquoise = (64, 224, 208, 200)
    Violet = (238, 130, 238, 200)
    Wheat = (245, 222, 179, 200)
    White = (255, 255, 255, 200)
    Whitesmoke = (245, 245, 245, 200)
    Yellow = (255, 255, 0, 200)
    Yellowgreen = (154, 205, 50, 200)

    def __init__(self, r, g, b, a):
        self.rgba = (r, g, b, a)

    def __call__(self):
        return self.rgba


# endregion [Data_2]


# region [Data_3]


# endregion [Data_3]


# region [Data_4]


# endregion [Data_4]


# region [Data_5]


# endregion [Data_5]


# region [Data_6]


# endregion [Data_6]


# region [Data_7]


# endregion [Data_7]


# region [Data_8]


# endregion [Data_8]


# region [Data_9]


# endregion [Data_9]


# region [Main_Exec]

if __name__ == '__main__':
    pass


# endregion [Main_Exec]
