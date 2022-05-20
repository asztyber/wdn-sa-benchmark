function [n,row] = LumpExt(m,row)

%m = LumpExt(m,1), the equivalence classes can be lumped together 
%in order to reduce the computational complexity of the algorithm

no_rows = size(m.sm,1);                  %no_rows: number of equations = 6
remRows = [1:row-1 row+1:no_rows];       %remRows = [0 2:6]=[2 3 4 5 6]
remRowsf = [1:row-1 row+1:length(m.f)];  %remrowsFaults=[0 2:5]=[2 3 4 5]
[row_just,row_over,col_over]=GetJustOver(m.sm(remRows,:));
merge = length(row_just)>0; %ind of the justDetPart

if merge   %if merge >0
    
    eqcls = [remRows(row_just) row]; %equivalence classes=eqcls=[2 1]
    no_rows_before_row = sum(eqcls < row); % = 0, for the first row
    row = row - no_rows_before_row;        %row= 1-0 =1
    no_rows_before = sum(eqcls < m.delrow);  % =0, for the first row
    n.delrow = m.delrow - no_rows_before;    %=1, n is the new m
    
    eqclsf = eqcls(eqcls<=length(m.f)); %eqclsf =[2 1] < = 5
    row_overf = row_over(row_over<=length(remRowsf)); %row_overf=[2 3 4]
    
    if no_rows_before > 0    %no_rows_before=0,ffr
        rowinsert = n.delrow;
    else
        rowinsert = row;      %rowinsert=1,ffr
    end
    n.sm = [m.sm(remRows(row_over(1:rowinsert-1)),col_over);...  %[null]
        any(m.sm(eqcls,col_over));...                            %[1 1]
        m.sm(remRows(row_over(rowinsert:end)),col_over)];        %[1 0;1 0;0 1;1 1]
    
    n.e = [m.e(remRows(row_over(1:rowinsert-1))) {[m.e{eqcls}]}... %[null] [2 1]
        m.e(remRows(row_over(rowinsert:end)))];                    %[4] [5] [6] [3]
    
    n.f = [m.f(remRowsf(row_overf(1:rowinsert-1))) {[m.f{eqclsf}]}... %[null] [2 1] 
        m.f(remRowsf(row_overf(rowinsert:end)))];                     %[3] [4] [5]
    
    n.sr = m.sr;
    
    if no_rows_before > 0 
        n.delrow = n.delrow+1;  %n.delrow=0, ffr
        %n.delrow =1; %modificación para que encuentre todos los MTES
    end
else
    n = m;   %new model
end
row = row + 1; %for the next row: fnr

