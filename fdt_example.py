import faultdiagnosistoolbox as fdt
import json

with open('examples/structural_models/TLN_7_0_7.json', 'r') as f:
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

model = fdt.DiagnosisModel(model_def, name='TLN')
model.Lint()

mtes = model.MTES()
print("number of TES: ", len(mtes))

isol = model.IsolabilityAnalysisArrs(mtes)
print('unambiguity groups: ', isol.sum(axis=1))

msos = model.MSO()
print("number of MSO: ", len(msos))
