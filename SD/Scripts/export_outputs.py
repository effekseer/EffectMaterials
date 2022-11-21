import sd
import sd.tools.export
from sd.api.sdproperty import SDPropertyCategory
from sd.api.sdvaluetexture import SDValueTexture

from pathlib import Path

def get_texture(node):
  prop = node.getProperties(SDPropertyCategory.Output)[0]
  value = node.getPropertyValue(prop)
  return SDValueTexture.get(value)

def get_identifer(node):
	return node.getAnnotationPropertyValueFromId('identifier').get()
	
pkg_manager = sd.getContext().getSDApplication().getPackageMgr()
graph_def_manager = sd.getContext().getSDApplication().getSDGraphDefinitionMgr()

for pkg in pkg_manager.getUserPackages():
  file_path = Path(pkg.getFilePath())
  for graph in pkg.getChildrenResources(False):
    if not hasattr(graph, 'compute'):
      continue
    graph.compute()
    for output_node in graph.getOutputNodes():
      identifer = get_identifer(output_node)
      texture = get_texture(output_node)
      dst_path = file_path.parent / (file_path.stem + '_' + identifer + '.png')
      texture.save(str(dst_path))
