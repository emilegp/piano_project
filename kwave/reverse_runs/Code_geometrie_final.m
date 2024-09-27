% code pour geo 1

for i = 1:Nx
    for j = 1:Ny
        if i > 15 && i < 25 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 15 && i < 75 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/1000))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 170 && i < 200 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 170 && i < 200 && j >= (Ny/4) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif  j >= (125+i/1.2)
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
 sourceGrid = [100, 100];
 sourceGrid = [50, 100];
 sourceGrid = [50, 25];

% code pour geo 2

for i = 1:Nx
    for j = 1:Ny
        % Condition pour les deux coupes inclinées
        if j <= (100 - i/1.5) || j >= (100 + i/1.5)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
    elseif i > 50 && i < 60 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 80 && i < 100 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end

% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3));  

%emplacement sources
 sourceGrid = [100, 50] ;
 sourceGrid = [25, 100];
 sourceGrid =[110, 150];
%code geo 3
for i = 1:Nx
    for j = 1:Ny
        if i > 50 && i < 75 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 100 && i < 120 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 50 && i < 70 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif j >= (120+i/1.2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
      
        end
    end
end
    
% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3)); 
  
%emplacement sources
 sourceGrid = [80, 150];
 sourceGrid = [20, 100];
 sourceGrid = [100, 30];



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
     if (i - (Nx - 200))^2 + (j - (Ny - 200))^2 > 200^2 
            medium.sound_speed(i,j) = airSpeed; 
            medium.density(i,j) = airDensity;    
        end
    end
end
%code geo 6

for i = 1:Nx
    for j = 1:Ny
        if i > 0 && i < 80 && j >= 0 && j <= (Ny/2)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 0 && i < 80 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/1000))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 100 && i < 120 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/3))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 100 && i < 120 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/5))
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
   elseif i > 100 && i < 110 && j >= (Ny/5) && j <= (Ny/3)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
 
        end
    end
end
    

% emplacements sensor
sensor_line_1 = round(Nx-(Nx /5));  
sensor_line_2 = round(Nx-(Nx /3)); 

 sourceGrid = [100, 30];
 sourceGrid = [100, 180];
 sourceGrid = [180, 100];

