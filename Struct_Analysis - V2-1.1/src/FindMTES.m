function S = FindMTES(m,p)
% Input: a structural model m with redundancy at least 1 and with at least
% one equ.class including faults.
% Cases:
% a) The sm has structural redundancy 1. No more removals are possible.
%    Store the equations and faults.
% b) The sm has redundancy more than 1.
%    i)  There are only one equ.class including faults. No more removals are
%        possilbe. Store the equations and the faults.
%    ii) There are more than one equ.class including faults. Store the PSO
%        if all PSOs are wanted. Remove allowed classes and make a
%        reqursive call.

% Check if m is an MTES
m = LumpExt(m,1);  % the equivalence classes can be lumped together in order to reduce the computational complexity of the algorithm
if length(m.f)==1 % if m is MTES
    S = storeFS(m); % then store m
else %otherwise make recursive call
    if p == 1
        S = storeFS(m);
    else
        S = initS;
    end
    row = m.delrow;
    while length(m.f)>=row % some rows are allowed to be removed
        [m,row] = LumpExt(m,row); % lump model w.r.t. row
    end
    for delrow = m.delrow:length(m.f)
        % create the model where delrow has been removed
        m.delrow = delrow;
        rows = [1:delrow-1 delrow+1:size(m.sm,1)];
        n = GetPartialModel(m,rows);
        
        Sn = FindMTES(n,p); % make recursive call
        S = addResults(S,Sn); % store results
    end   
end

