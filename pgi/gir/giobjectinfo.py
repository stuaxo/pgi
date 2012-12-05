# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import c_char_p, CFUNCTYPE, c_void_p

from pgi.glib import gchar_p, gboolean, gint
from pgi.gobject import GValuePtr
from gibaseinfo import GIInfoType
from giinterfaceinfo import GIInterfaceInfoPtr
from gifieldinfo import GIFieldInfoPtr
from gipropertyinfo import GIPropertyInfoPtr
from gicallableinfo import GIFunctionInfoPtr, GISignalInfoPtr, GIVFuncInfoPtr
from giregisteredtypeinfo import GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr
from giconstantinfo import GIConstantInfoPtr
from gistructinfo import GIStructInfoPtr
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_object_info(base_info, _type=GIInfoType.OBJECT):
    return base_info.get_type().value == _type


class GIObjectInfo(GIRegisteredTypeInfo):
    pass


class GIObjectInfoPtr(GIRegisteredTypeInfoPtr):
    _type_ = GIObjectInfo

    def get_methods(self):
        return map(self.get_method, xrange(self.get_n_methods()))

    def get_interfaces(self):
        return map(self.get_interface, xrange(self.get_n_interfaces()))

    def get_properties(self):
        return map(self.get_property, xrange(self.get_n_properties()))

    def get_signals(self):
        return map(self.get_signal, xrange(self.get_n_signals()))

    def get_vfuncs(self):
        return map(self.get_vfunc, xrange(self.get_n_vfuncs()))

    def get_fields(self):
        return map(self.get_field, xrange(self.get_n_fields()))

    def _get_repr(self):
        values = super(GIObjectInfoPtr, self)._get_repr()
        values["type_name"] = repr(self.get_type_name())
        values["type_init"] = repr(self.get_type_init())
        values["abstract"] = repr(self.get_abstract())
        values["fundamental"] = repr(self.get_fundamental())
        parent = self.get_parent()
        if parent:
            values["parent"] = repr(parent.get_name())
            parent.unref()
        values["n_interfaces"] = repr(self.get_n_interfaces())
        values["n_fields"] = repr(self.get_n_fields())
        values["n_properties"] = repr(self.get_n_properties())
        values["n_methods"] = repr(self.get_n_methods())
        values["n_signals"] = repr(self.get_n_signals())
        values["n_vfuncs"] = repr(self.get_n_vfuncs())
        class_struct = self.get_class_struct()
        values["class_struct"] = repr(class_struct.get_name())
        class_struct.unref()
        unref_function = self.get_unref_function()
        if unref_function:
            values["unref_function"] = repr(unref_function)
        ref_function = self.get_ref_function()
        if ref_function:
            values["ref_function"] = repr(ref_function)
        set_value_function =  self.get_set_value_function()
        if set_value_function:
            values["set_value_function"] = repr(set_value_function)
        get_value_function = self.get_get_value_function()
        if get_value_function:
            values["get_value_function"] = repr(get_value_function)
        return values


GIObjectInfoGetValueFunction = CFUNCTYPE(c_void_p, GValuePtr)
GIObjectInfoRefFunction = CFUNCTYPE(c_void_p, c_void_p)
GIObjectInfoSetValueFunction = CFUNCTYPE(None, GValuePtr, c_void_p)
GIObjectInfoUnrefFunction = CFUNCTYPE(None, c_void_p)

_methods = [
    ("get_type_name", gchar_p, [GIObjectInfoPtr]),
    ("get_type_init", gchar_p, [GIObjectInfoPtr]),
    ("get_abstract", gboolean, [GIObjectInfoPtr]),
    ("get_fundamental", gboolean, [GIObjectInfoPtr]),
    ("get_parent", GIObjectInfoPtr, [GIObjectInfoPtr]),
    ("get_n_interfaces", gint, [GIObjectInfoPtr]),
    ("get_interface", GIInterfaceInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_fields", gint, [GIObjectInfoPtr]),
    ("get_field", GIFieldInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_properties", gint, [GIObjectInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_methods", gint, [GIObjectInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIObjectInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIObjectInfoPtr, gchar_p]),
    ("get_n_signals", gint, [GIObjectInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_vfuncs", gint, [GIObjectInfoPtr]),
    ("get_vfunc", GIVFuncInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_n_constants", gint, [GIObjectInfoPtr]),
    ("get_constant", GIConstantInfoPtr, [GIObjectInfoPtr, gint]),
    ("get_class_struct", GIStructInfoPtr, [GIObjectInfoPtr]),
    ("find_vfunc", GIVFuncInfoPtr, [GIObjectInfoPtr, gchar_p]),
    ("get_unref_function", c_char_p, [GIObjectInfoPtr]),
    ("get_unref_function_pointer", GIObjectInfoUnrefFunction,
        [GIObjectInfoPtr]),
    ("get_ref_function", c_char_p, [GIObjectInfoPtr]),
    ("get_ref_function_pointer", GIObjectInfoRefFunction, [GIObjectInfoPtr]),
    ("get_set_value_function", c_char_p, [GIObjectInfoPtr]),
    ("get_set_value_function_pointer", GIObjectInfoSetValueFunction,
        [GIObjectInfoPtr]),
    ("get_get_value_function", c_char_p, [GIObjectInfoPtr]),
    ("get_get_value_function_pointer", GIObjectInfoGetValueFunction,
        [GIObjectInfoPtr]),
]

wrap_class(_gir, GIObjectInfo, GIObjectInfoPtr, "g_object_info_", _methods)

__all__ = ["GIObjectInfo", "GIObjectInfoPtr", "gi_is_object_info",
           "GIObjectInfoGetValueFunction", "GIObjectInfoRefFunction",
           "GIObjectInfoSetValueFunction", "GIObjectInfoUnrefFunction"]
