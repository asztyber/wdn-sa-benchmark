%% Case Study: TLN_7_0_7
clc
clear all
addpath('Struct_Analysis - V2-1.1')
addpath('src')

fname = 'TLN_7_0_7.json'; 
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
val = jsondecode(str);

%%
rels = struct2cell(val.model);
for i=1:length(rels)
    rels{i}=rels{i}';
end
relsX=rels';

Xvar=val.unknown;
Fvar=val.faults;
Zvar=val.known;

% Compute the incidence matrices
X = symbdef(relsX, Xvar)>0;
F = symbdef(relsX, Fvar)>0;
Z = symbdef(relsX, Zvar)>0;


% Build SM object
SM      = CreateSM(X,F,Z,{},Xvar,Fvar,Zvar); 
SM.name = fname;
figure(1)
PlotSM(SM)

GL_MSO = MSO(SM)
GL_FMSO = FMSO(SM)
