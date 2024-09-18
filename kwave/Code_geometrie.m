% code pour deo 1
for i = 1:Nx
    for j = 1:Ny
        if i > 20 && i < 30 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 70 && i < 80 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/6))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 0 && i < 70 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/100))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity
   elseif  j >= (64+i/1.2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
  elseif  j <= (1+i/10)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end
    

% code pour geo 2
for i = 1:Nx
    for j = 1:Ny
        if i > 60 && i < 70 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 40 && i < 45 && j >= (Ny - (Ny/2.2)) && j <= (Ny - (Ny/2.4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
    elseif  j <= (60-i/1.5)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif  j >= (64+i/1.5)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end
    




%code geo 3
for i = 1:Nx
    for j = 1:Ny
        if i > 20 && i < 30 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 70 && i < 80 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/3))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 50 && i < 55 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity
   elseif  j >= (80+i/1.5)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
      
        end
    end
end
    
%geo 4 avec aucune contrainte (carre)


% geo 5 
for i = 1:Nx
    for j = 1:Ny 
     if (i - (Nx - 90))^2 + (j - (Ny - 90))^2 > 90^2 
            medium.sound_speed(i,j) = airSpeed; 
            medium.density(i,j) = airDensity;    
        end
    end
end