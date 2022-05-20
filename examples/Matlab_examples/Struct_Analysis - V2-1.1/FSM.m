function V=FSM(faults,FMSO)
%G.Perez 11/2015
%Función para calcular la matriz de firma de fallas> FMSO vs faults
%faults tiene el formato faults=[ x x x ...]
%FMSO={[x x x], [x x x],...}
%faults es el vector que contiene las ecuaciones con fallas

 V=zeros(length(FMSO),length(faults));

for i=1:length(FMSO) 
  for j=1:length(faults)
    if ismember(faults(j),FMSO{i}) == 1; % si 1 o + elementos de faults esta en el 1er,2do,etc MSO...
        V(i,j)= 1;
    end
  end
end
