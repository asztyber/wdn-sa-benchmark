function S = FindFMSO(sm,eqf,p)

% FindFMSO  Through structural analysis obtain all  FMSOs
%
%    S = FindMSO(sm,eqf,p)
%
%  Inputs:
%      - sm   A structural model of the unnknown variables represented with
%             its biadjacency matrix.
%      - eqf  equations with faults
%
%      - p    If p is true all PSO sets are also stored in the output
%             S.PSOs. The default value is false.
%
%  Outputs:
%
%    S.FMSOs      - The family of all FMSO sets in sm.
%
%
% Author(s): Gustavo Pérez, Elodie Chanthery, Louise Travé-Massuyès
% Date: 15/06/2016 Copyright (C) 2016 
%
% Author(s): Gustavo Pérez, Elodie Chnathery, Louise Travé-Massuyès
% Revision: 0.2, Date: 15/06/2016 Copyright (C) 2016 
% Copyright (C) 2016 Gustavo Pérez, Elodie Chnathery, Louise Travé-Massuyès
%
% This file is un upgrade of TestModTool of Matias Krysander
% You should have received a copy of the GNU General Public License along
% with FindMSO; if not, write to the Free Software Foundation, Inc.,
% 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
% eqf
% FMSOs=[];
% FMSOf=[];
% FMSO_SM=[];

global withPSO
if nargin<2
    withPSO = 0;
else
    withPSO = p;
end

[row_over,col_over]=Mp(sm); %Computes the overdetermined part.
sr = length(row_over)-length(col_over);

S.FMSOs = {};

if withPSO
        S.PSOs = {};
end
if sr > 0
    sm = sm(row_over,col_over);
    for i=1:length(row_over)
        M{i} = row_over(i);
    end
    delM = 1;
    no_classes = length(M);
    S.FMSOs = {};
    
    G = sub(sm,M,sr,delM,no_classes,eqf); %To find MSOs
    S.FMSOs =FMSO(eqf,G.MSOs);
end


function S = sub(sm,M,sr,delM,no_classes,eqff)
% A subroutine to FindMSO
global withPSO

if withPSO 
    S.PSOs = {[M{:}]};
end
if sr==1
    S.MSOs = {[M{:}]};
else
    S.MSOs = {};
    Mesleft = no_classes - delM + 1;

    if withPSO 
        psi = Mesleft-1;
    else
        psi = Mesleft - sr + 1;
    end
    
    while psi >= 0
        idxM = [1:delM-1 delM+1:no_classes];
        [row_just,row_over,col_over]=GetJustOver(sm(idxM,:));

        merge = length(row_just)>0;

        if merge
            no_rows_before = sum(row_just < delM);
            Mesleft = Mesleft - (length(row_just) - no_rows_before);

            if withPSO | sr-1<=Mesleft
                mergeclasses = [idxM(row_just) delM];
                delM = delM - no_rows_before;
                sm =[sm(idxM(row_over(1:delM-1)),col_over);...
                    any(sm(mergeclasses,col_over));...
                    sm(idxM(row_over(delM:end)),col_over)];
                M = [M(idxM(row_over(1:delM-1))) {[M{mergeclasses}]}...
                    M(idxM(row_over(delM:end)))];
                no_classes = no_classes - length(row_just);
                if no_rows_before==0
                    idxM = [1:delM-1 delM+1:no_classes];
                    Sn=sub(sm(idxM,:),M(idxM),sr-1,delM,no_classes-1,eqff);
                    S.MSOs=[S.MSOs Sn.MSOs];
                    if withPSO 
                        S.PSOs =[S.PSOs Sn.PSOs];
                    end
                end
                delM=delM+1;
                Mesleft = no_classes - delM + 1;
                if withPSO 
                    psi = Mesleft-1;
                else
                    psi = Mesleft - sr + 1;
                end
            else
                break;
            end
        else
            Sn=sub(sm(idxM,:),M(idxM),sr-1,delM,no_classes-1,eqff);
         
               
            S.MSOs=[S.MSOs Sn.MSOs];
            
            if withPSO 
                S.PSOs =[S.PSOs Sn.PSOs];
            end
            delM=delM+1;
            Mesleft = no_classes - delM + 1;
            if withPSO 
                psi = Mesleft-1;
            else
                psi = Mesleft - sr + 1;
            end
        end
    end
   
  

end

function F=FMSO(eqff,MSOs)
% %G.Perez revision 01/2016
% % FMSOs=FMSO2(faults,MSO)
% %faults vector is faults=[ x x x ...]
% %MSO vector is MSO={[x x x], [x x x],...}
% %faults is the vector that contains the equations with faults
 FMSOs=[];
 FMSOf=[];
 FMSO_SM=[];
% 

F.eq=[];
for i=1:length(MSOs) 
    indexfaults=ismember(eqff,MSOs{i});
  if sum(indexfaults)>= 1; 
    FMSOs= [FMSOs {sort(MSOs{i})} ]; 
    FMSOf=[FMSOf {find(indexfaults==1)} ];
    FMSO_SM=[FMSO_SM {indexfaults}];
  end
end

F.eq = FMSOs;
F.f= FMSOf;
F.SM= FMSO_SM;




function [row_just,row_over,col_over]=GetJustOver(sm)
%   Computes the just and over determined part of a structural
%              matrix. 
%
%    [row_just,row_over,col_over]=GetJustOver(sm)
%
%  Inputs:
%    sm  - A biadjacency matrix with a non-empty structurally
%                 overdetermined part and an empty structurally underdetermined part. 
%
%  Output:
%    row_just   - The row indices of the just-determind part.
%    row_over   - The row indices of the overdetermined part. 
%    col_over   - The column indices of the overdetermined part.
if ~size(sm,2)
    col_over = [];
    row_just = [];
    row_over = 1:size(sm,1);
else
    [p,q,r,s]=dmperm(sm);

    %last component
    rtmp=[r(end-1):r(end)-1];
    k=[s(end-1):s(end)-1];
    row_over = sort(p(rtmp)); % behövs detta
    col_over = q(k);

    %all but the last component
    r=[1:r(end-1)-1];
    row_just = p(r);
end



function [row_over,col_over]=Mp(sm)
%   Computes the overdetermined part of a structural
%              matrix. 
%
%    [row_over,col_over]=Mp(sm)
%
%  Inputs:
%    sm  - A biadjacency matrix. 
%
%  Output:
%    row_over   - The row indices of the overdetermined part. 
%    col_over   - The column indices of the overdetermined part.
if ~size(sm,2)
    col_over = [];
    row_over = 1:size(sm,1);
else
    [p,q,r,s]=dmperm(sm);
    rtmp=[r(end-1):r(end)-1];
    k=[s(end-1):s(end)-1];
    if length(rtmp) > length(k) % if overdetermined part exist
        row_over = sort(p(rtmp)); % behövs detta
        col_over = q(k);
    else
        row_over = [];
        col_over = [];
    end
end

