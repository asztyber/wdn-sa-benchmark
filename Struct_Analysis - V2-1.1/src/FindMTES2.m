function S = FindMTES2(m,p)
      
    S = initS;
    
    for row=1:length(m.f)
      [m,row] = LumpExt(m,row); % lump model w.r.t. row
    
      if length(m.f)==1 % if m is MTES
      S = storeFS(m); % then store m
      end
          
    end
    
    for delrow = m.delrow:length(m.f)
        m.delrow = delrow;
        rows = [1:delrow-1 delrow+1:size(m.sm,1)];
        n = GetPartialModel(m,rows);
        
        Sn = FindMTES2(n,p); % make recursive call
        S = addResults(S,Sn); % store results
    end


