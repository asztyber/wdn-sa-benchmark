function [row_just,row_over,col_over]=GetJustOver(sm)
%Get the Just and Over determined part of a structural matrix
%
%   Inputs: sm  - A biadjacency matrix with a non-empty structurally
%          overdetermined part and an empty structurally underdetermined
%          part. 
%   Output: row_just   - The row indices of the just-determind part.
%           row_over, col_over   - The row and columns indices of the overdetermined part. 

if ~size(sm,2) %if not exist variables unknowns
    col_over = [];
    row_just = [];
    row_over = 1:size(sm,1);
else
    [p,q,r,s]=dmperm(sm); %p =[1 2 4 3 5],q =[1 2 3],r =[1 2 6],s =[1 2 4]
    %last component
    rtmp=[r(end-1):r(end)-1]; %rtmp =[2 3 4 5]
    k=[s(end-1):s(end)-1];    %k=[2 3]
    if length(rtmp)~=length(k) %If the lengths are not equal
        row_over = sort(p(rtmp)); %p(rtmp)=[2 4 3 5], row_over=[2 3 4 5]
        col_over = q(k);          %col_over=[2 3]; ind of the overDetPart
        %all but the last component
        r=[1:r(end-1)-1]; % JUSTDETERMINED PART r= 1:(r(2)-1)=[1]
        row_just = p(r); %  row_just=[1]=ind of the justDetPart
    else
        row_over = [];
        col_over = [];
        row_just = [1:size(sm,1)];
    end
end