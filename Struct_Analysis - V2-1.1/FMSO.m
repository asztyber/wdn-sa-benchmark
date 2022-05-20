function [S] = FMSO(SM)
% Update for FSMO: Gustavo Pérez, Elodie Chnathery, Louise Travé-Massuyès
% Author(s) for MSO: Mattias Krysander, Erik Frisk

eqfaults=[];
for i=1:length(SM.F(1,:))
eqfaults= [eqfaults find(SM.F(:,i))];
end


fidx=zeros(1,size(SM.X,1));
for k=1:length(fidx)
  fk = find(SM.F(k,:)>0);
  if ~isempty(fk)
    fidx(k)=fk;
  end
end

S = FindFMSO(SM.X,eqfaults,0);