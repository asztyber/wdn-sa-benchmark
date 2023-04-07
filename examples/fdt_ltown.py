import faultdiagnosistoolbox as fdt
import json

with open('structural_models/L-TOWN_simplified_34_3_15.json', 'r') as f:
    data = json.load(f)

sm = data['model']
print('sm: ', sm)
relsX = [sm[e] for e in sorted(sm.keys(), key=lambda x: int(x[1:]))]
model_def = {
    'type': 'VarStruc',
    'x': data['unknown'],
    'z': data['known'],
    'f': data['faults'],
    'rels': relsX
}

print('unknown: ', model_def['x'])
print('known: ', model_def['z'])
print('faults: ', model_def['f'])

model = fdt.DiagnosisModel(model_def)
model.Lint()

mtes = model.MTES()
print("number of TES: ", len(mtes))

mtes = [[int(x) for x in list(m)] for m in mtes]
lengths = [len(m) for m in mtes]
print(lengths)
file_name = 'output/ltown_mtes.json'
with open(file_name, 'w') as f:
    json.dump(mtes, f)

isol = model.IsolabilityAnalysisArrs(mtes)
print('unambiguity groups: ', isol.sum(axis=1))

# msos = model.MSO()
# print("number of MSO: ", len(msos))
