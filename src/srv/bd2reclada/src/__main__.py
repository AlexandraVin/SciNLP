import json
import csv
import sys
import uuid
from .bdtypes import get_obj_type, field_names


with open(sys.argv[1]) as inputfile:
    inputobj = json.load(inputfile)
objects = []
queue = [inputobj]
inputobj['id'] = str(uuid.uuid4())
while queue:
    obj = queue.pop(0)
    qpos = 0
    if not isinstance(obj, dict):
        continue
    obj_type = get_obj_type(obj)
    robj = {}
    if obj_type is not None:
        robj['class'] = obj_type[0].upper() + obj_type[1:]
    _ = lambda f: field_names.get((obj_type, f), f)
    objects.append(robj)
    robj['id'] = obj['id']
    robj = robj.setdefault('attrs', {})
    for k, v in obj.items():
        if k == 'id':
            continue
        if isinstance(v, list):
            if obj_type is None or any(not isinstance(item, dict) for item in v):
                robj[_(k)] = rlist = []
            for item in v:
                if isinstance(item, dict):
                    queue.insert(qpos, item)
                    qpos += 1
                    item['id'] = str(uuid.uuid4())

                    if obj_type is None:
                        rlist.append(item['id'])
                    else:
                        item[obj_type] = obj['id']
                else:
                    rlist.append(item)
        elif isinstance(v, dict):
            v['id'] = str(uuid.uuid4())
            queue.insert(qpos, v)
            qpos += 1
            robj[_(k)] = v['id']
        else:
            robj[_(k)] = v
with open(sys.argv[2], 'w') as outfile:
    writer = csv.writer(outfile, quotechar='\'')
    for obj in objects:
        writer.writerow([json.dumps(obj, indent=4)])
