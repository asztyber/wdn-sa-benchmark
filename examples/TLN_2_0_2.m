%% Case Study: TLN_2_0_2

% clc
% clear all
addpath('Struct_Analysis - V2-1.1')
addpath('src')

fname = 'TLN_2_0_2.json'; 
fid = fopen(fname)
raw = fread(fid,inf)
str = char(raw')
fclose(fid)
val = jsondecode(str)

%%
C = struct2cell(val.model);
for i=1:length(C)
    C{i}=C{i}';
end
relsX=C';

Xvar=val.unknown;
Fvar=val.faults;
Zvar=val.known;

% Compute the incidence matrices
X = symbdef(relsX, Xvar)>0;
F = symbdef(relsX, Fvar)>0;
Z = symbdef(relsX, Zvar)>0;


% Build SM object
SM      = CreateSM(X,F,Z,{},Xvar,Fvar,Zvar); 
SM.name = 'TLN_2_0_2';
figure(1)
PlotSM(SM)

GL_MSO = MSO(SM)
%GL_FMSO = FMSO(SM)
