# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.glib import Enum, gchar_p, gboolean, gint
from gibaseinfo import GIInfoType, GIBaseInfo, GIBaseInfoPtr
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_type_info(base_info, _type=GIInfoType.TYPE):
    return base_info.get_type().value == _type


class GIArrayType(Enum):
    C, ARRAY, PTR_ARRAY, BYTE_ARRAY = range(4)


class GITypeTag(Enum):
    VOID = 0
    BOOLEAN = 1
    INT8 = 2
    UINT8 = 3
    INT16 = 4
    UINT16 = 5
    INT32 = 6
    UINT32 = 7
    INT64 = 8
    UINT64 = 9
    FLOAT = 10
    DOUBLE = 11
    GTYPE = 12
    UTF8 = 13
    FILENAME = 14
    ARRAY = 15
    INTERFACE = 16
    GLIST = 17
    GSLIST = 18
    GHASH = 19
    ERROR = 20
    UNICHAR = 21

    def is_basic(self):
        return (self.value < self.ARRAY or self.value == self.UNICHAR)

_methods = [
    ("to_string", gchar_p, [GITypeTag]),
]

wrap_class(_gir, GITypeTag, None, "g_type_tag_", _methods)


class GITypeInfo(GIBaseInfo):
    pass


class GITypeInfoPtr(GIBaseInfoPtr):
    _type_ = GITypeInfo

    def _get_repr(self):
        values = super(GITypeInfoPtr, self)._get_repr()
        values["is_pointer"] = repr(self.is_pointer())
        tag = self.get_tag()
        values["tag"] = repr(tag)
        if tag.value == GITypeTag.INTERFACE:
            interface = self.get_interface()
            values["interface"] = repr(interface)
            interface.unref()
        elif tag.value == GITypeTag.ARRAY:
            values["array_length"] = repr(self.get_array_length())
            values["array_fixed_size"] = repr(self.get_array_fixed_size())
            values["zero_terminated"] = repr(self.is_zero_terminated())
            values["array_type"] = repr(self.get_array_type())
        return values


_methods = [
    ("is_pointer", gboolean, [GITypeInfoPtr]),
    ("get_tag", GITypeTag, [GITypeInfoPtr]),
    ("get_param_type", GITypeInfoPtr, [GITypeInfoPtr, gint]),
    ("get_interface", GIBaseInfoPtr, [GITypeInfoPtr]),
    ("get_array_length", gint, [GITypeInfoPtr]),
    ("get_array_fixed_size", gint, [GITypeInfoPtr]),
    ("is_zero_terminated", gboolean, [GITypeInfoPtr]),
    ("get_array_type", GIArrayType, [GITypeInfoPtr]),
]

wrap_class(_gir, GITypeInfo, GITypeInfoPtr, "g_type_info_", _methods)

__all__ = ["GIArrayType", "GITypeTag", "GITypeInfo", "GITypeInfoPtr",
           "gi_is_type_info"]
