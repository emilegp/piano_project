function test_geo(Nx, Ny, dx, dy, med, shape, ...
    sensorid, sourceid)
%RUN Summary of this function goes here
%   Detailed explanation goes here

% Definition des propriété de base du matériau de propagation
medium.sound_speed = med.SoundSpeed * ones(Nx, Ny); % Change SoundSpeed to sound_speed
medium.density = med.Density * ones(Nx, Ny); % Change Density to density

% Definition des propriétés de simulation 
% (Ne pas toucher)
medium.alpha_coeff = 0.75;              % [dB/(MHz^y cm)]
medium.alpha_power = 1.5;

airSpeed = 330;     % [m/s]
airDensity = 10;    % [kg/m^3]

kgrid = kWaveGrid(Nx, dx, Ny, dy);

%% Air autour du matériau
for i = 1:Nx
    for j = 1:Ny
        if i < 4 || i > (Nx-4) || j < 4 || j > (Ny-4)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end

%% Définition de la géométrie selon le label shape
if shape == 1
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
                medium.density(i,j) = airDensity;
            elseif j >= (64 + i/1.2)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            elseif j <= (1 + i/10)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            end
        end
    end
elseif shape == 2
    for i = 1:Nx
        for j = 1:Ny
            if i > 60 && i < 70 && j >= (Ny/5) && j <= (Ny/3)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            elseif i > 40 && i < 45 && j >= (Ny - (Ny/2.2)) && j <= (Ny - (Ny/2.4))
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            elseif j <= (60 - i/1.5)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            elseif j >= (64 + i/1.5)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            end
        end
    end
elseif shape == 3
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
                medium.density(i,j) = airDensity;
            elseif j >= (80 + i/1.5)
                medium.sound_speed(i,j) = airSpeed;
                medium.density(i,j) = airDensity;
            end
        end
    end
% shape == 4 ou autre résulte en un carré plein, test de symétrie
elseif shape == 5
    for i = 1:Nx
        for j = 1:Ny 
            if (i - (Nx - 8))^2 + (j - (Ny - 8))^2 > 8^2 
                medium.sound_speed(i,j) = airSpeed; 
                medium.density(i,j) = airDensity;    
            end
        end
    end
end

%% Placement du sensor

sensor_loc = med.sensorlocs(sensorid, :);

sensorXGrid = [sensor_loc(1)];     % [gridPoint]
sensorYGrid = [sensor_loc(2)];     % [gridPoint]

sensor.mask = [kgrid.x_vec(sensorXGrid)'; kgrid.y_vec(sensorYGrid)'];

%% Placement de la source

source_loc = med.sourcelocs(sourceid, :);

sourceGrid = [source_loc(1), source_loc(2)];

source_x_pos = kgrid.x_vec(sourceGrid(1));         % [grid points]
source_y_pos = kgrid.y_vec(sourceGrid(2));         % [grid points]

%% Visualisation de la grille de simulation
% On peut s'assurer que tous nos paramètres sont correctement définis à
% l'aide d'un graphique.

figure;
imagesc(kgrid.y_vec * 1e3, kgrid.x_vec * 1e3, medium.sound_speed); axis image
ylabel('y - position [mm]')
xlabel('x - position [mm]')
c = colorbar;
c.Label.String = 'Speed of sound';
hold on;
plot(sensor.mask(2, :) * 1e3, sensor.mask(1, :) * 1e3, 'r.')
plot(source_y_pos * 1e3, source_x_pos * 1e3, 'b+')
legend('Sensor', 'Source')

end