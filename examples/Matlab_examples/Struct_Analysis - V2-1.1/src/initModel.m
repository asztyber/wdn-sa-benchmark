function m = initModel(sm,f)
% Author(s): Mattias Krysander, Erik Frisk
% Revision: 0.1, Date: 2010/08/19
%
% Copyright (C) 2010 Mattias Krysander and Erik Frisk

% This file is part of TestModTool.
% 
% TestModTool is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or
% (at your option) any later version.
% 
% TestModTool is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%   
% You should have received a copy of the GNU General Public License along
% with TestModTool; if not, write to the Free Software Foundation, Inc., 51
% Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[row_over,col_over,m.sr]=Mp(sm); 
f = f(row_over);           %f=faults/eqM+ = f =    1   2   0   3   4   5 
idxf = find(f);            % Find indices only of faults elements.
idx = [idxf setdiff([1:length(row_over)],idxf)];% setdiff=row_over-idxf
f = f(idx);                 %idx=[1 2 4 5 6 3], f=[1 2 3 4 5 0]
row_over = row_over(idx);    % row_over=[1 2 4 5 6 3]

m.sm = sm(row_over,col_over); %m.sm([1 2 4 5 6 3],[1 2 3])
m.f = {};
for i=1:length(idxf)
    m.f{i} = f(i);            %assigns the number of faults
end
m.e = {};
for i=1:length(row_over)
    m.e{i} = row_over(i);     %equations of fault, in the order of row_over
end
m.delrow = 1;                 %initializes delrow=1?
