function [S] = MTES(SM)
% MTES -  finds all Minimal Test Equation Sets and Minimal Test Sets in
% a structural model.
%
%     [S] = MTES(SM)
%
%  Inputs:
%    SM     - A structural model in the SM format
%
%  Output:
%    S.eq   - cell array of TES represented as index sets. 
%    S.f    - cell array of TS represented as index sets.
%    S.sr   - vector with the structural redundancy of each TES.


fidx=zeros(1,size(SM.X,1)); %fidx = 0   0   0   0   0   0
for k=1:length(fidx)
  fk = find(SM.F(k,:)>0);  %number de fault for each equation,
  if ~isempty(fk)          %each fault variables only appear in 1 equation only
    fidx(k)=fk;            %fidx is updated with the corresponding fault:
  end                      %fidx =    1   2   0   3   4   5
end
S = TESsub(SM.X,fidx,0);
