function x = loc_shar( rels,subs )
%determinar variables desconocidas locales y compartidas de un sistema de tipo relsX
%se debe incluir el sistema y las ecuaciones de cada subsistema
% subs={[1 2 3 4 5 6 7] [8 9 10 11 12 13 14 15 16] [17 18 19 20 21 22 23 24 25] [26 27 28 29 30 31 32 33 34] [35 36 37 38 39 40]}


for i=1:length(subs)
   x(i)={[]};    
end

for i=1:length(subs) % desde el subsistema 1 hasta el total de subsistemas
    
   y=[];     
   for j=1:length(subs{i}) %desde la ecuación 1 hasta el total de ecuaciones del subsistema
    
    y=union(rels{subs{i}(j)},y);
    
   end
    x(i)={y};
    
 
end
xs={};

for k=1:length(subs)
    
    for l=k+1:length(subs)
       
        if k < l    
            xs=union(intersect(x{k},x{l}),xs);
        end
    
    end
end


end

