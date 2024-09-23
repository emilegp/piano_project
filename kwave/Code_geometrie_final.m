% code pour geo 1
for i = 1:Nx
    for j = 1:Ny
        if i > 30 && i < 50 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 30 && i < 150 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/1000))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 360 && i < 400 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 360 && i < 400 && j >= (Ny/4) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif  j >= (300+i/1.2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
  elseif  j <= (2+i/8)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end
    
% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3));  

%emplacement sources
 sourceGrid = [100, 100]
 sourceGrid = [200, 350];
 sourceGrid = [30, 200];

% code pour geo 2

for i = 1:Nx
    for j = 1:Ny
        % Condition pour les deux coupes inclinées
        if j <= (200 - i/1.5) || j >= (200 + i/1.5)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
    elseif i > 100 && i < 130 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 200 && i < 240 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end

% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3));  

%emplacement sources
 sourceGrid = [80, 200];
 sourceGrid = [200, 200];
 sourceGrid = [250, 80];

%code geo 3
for i = 1:Nx
    for j = 1:Ny
        if i > 100 && i < 130 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 200 && i < 240 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 100 && i < 180 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif j >= (300+i/1.2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
      
        end
    end
end
% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3)); 
  
%emplacement sources
 sourceGrid = [50, 100];
 sourceGrid = [200, 370];
 sourceGrid = [100, 300];



%geo 4 avec aucune contrainte (carre)
% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3)); 

 sourceGrid = [80, 200];
 sourceGrid = [200, 200];
 sourceGrid = [250, 80];

% geo 5 (est-ce qu<on la fait vrm???)
for i = 1:Nx
    for j = 1:Ny 
     if (i - (Nx - 14.5))^2 + (j - (Ny - 14.5))^2 > 14.5^2 
            medium.sound_speed(i,j) = airSpeed; 
            medium.density(i,j) = airDensity;    
        end
    end
end

%code geo 6

for i = 1:Nx
    for j = 1:Ny
        if i > 0 && i < 150 && j >= 0 && j <= (Ny/2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 0 && i < 150 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/1000))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 200 && i < 252 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/3))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 200 && i < 252 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 340 && i < 380 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
 
        end
    end
end

% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3)); 

 sourceGrid = [300, 300];
 sourceGrid = [200, 100];
 sourceGrid = [220, 175];

