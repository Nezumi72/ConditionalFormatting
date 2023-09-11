bl_info = {
    "name": "Conditional formatting",
    "author": "Nezumi",
    "version": (0, 0, "4a"),
    "blender": (3, 6, 1),
    "location": "View3D > UI > C-Format",
    "description": "Conditional formatting",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

import sys
import importlib
import os
import bpy


addon_path = os.path.dirname(os.path.realpath(__file__))
modulesNames = []
folders = ['properties', 'operators', 'panels']
for folder in folders:
    for mod in os.listdir(os.path.join(addon_path, folder)):
        if mod.endswith('.py'):
            modulesNames.append(f"{folder}.{mod[:-3]}")

modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
    for handler in bpy.app.handlers.depsgraph_update_post:
        if hasattr(handler, "conditional"):
            bpy.app.handlers.depsgraph_update_post.remove(handler)
            break
