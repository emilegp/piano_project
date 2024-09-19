%% Clear
clear all; clc

%% Simulation grid parameter
% Dimensions du medium
Mx = 19;        % minimum approx 10
My = 19;        % minimum approx 10

% Taille réelle de la simulation

Nx = Mx + 7;               % number of grid points in the x (row) direction
Ny = My + 7;               % number of grid points in the y (column) direction
dx = 5e-3;            % grid points spacing in the x direction [m]
dy = 5e-3;            % grid points spacing in the y direction [m]

kgrid = kWaveGrid(Nx, dx, Ny, dy);

SoundSpeed = 3000;      % Sound speed in the main material [m/s]
Density = 2500;         % Density of the main material [kg/m^3]


%% Changement du pas de temps

% % Optional, if set manually, both must be changed
% % -->
% % Attention le rapport entre la vitesse du son et le "dt" ne doit pas
% % être en dessous de ~5*10^9 pour eviter des erreurs numeriques.
% 
%
% kgrid.Nt = 8000;      % number of time steps
% kgrid.dt = 5*10^-7;   % time step [s]


%% Shape of the medium

% Definition des propriété de base du matériau de propagation
medium.sound_speed = SoundSpeed*ones(Nx, Ny);
medium.density = Density*ones(Nx, Ny);

% Definition des propriétés de simulation 
% (Ne pas toucher)
medium.alpha_coeff = 0.75;              % [dB/(MHz^y cm)]
medium.alpha_power = 1.5;


% Afin d'avoir une onde qui se reflete aux extremites, une partie du
% domaine doit avoir les caractéristiques de l'air. Donc :
% Vitesse du son : 330 m/s
% Densité : 10 kg/m^3 (Pas exactement comme l'air mais evite des erreurs numeriques)

airSpeed = 330;     % [m/s]
airDensity = 10;    % [kg/m^3]

for i = 1:Nx
    for j = 1:Ny
        if i < 4 || i > (Nx-4) || j < 4 || j > (Ny-4)
            medium.sound_speed(i,j) = airSpeed;
            medium.density(i,j) = airDensity;
        end
    end
end

% Trous aux coordonnées suivantes (dans le medium)
holes = [
    3,12; 3,13; 3,14
    4,12; 4,13; 4,14;
    5,12; 5,13; 5,14
];

for k = 1:size(holes, 1)
    i = holes(k, 1) + 3;
    j = holes(k, 2) + 3;
    medium.sound_speed(i,j) = airSpeed;
    medium.density(i,j) = airDensity;
end

%% Define sensor
% On définit les capteurs de l'onde acoustique. On peut en definir
% plusieurs d'un même coup en ajoutant une paire de coordonnée sur la
% grille de simulation

clear sensor

%position du sensor dans le medium
sensorPosx = 5;
sensorPosy = 4;

sensorXGrid = [sensorPosx+3];     % [gridPoint]
sensorYGrid = [sensorPosy+3];     % [gridPoint]

% On transforme les points de la grille de simulation en position
% cartésienne.

sensor.mask = [kgrid.x_vec(sensorXGrid)'; kgrid.y_vec(sensorYGrid)'];

%% Source definition
% De même, la source est défini grâce à une paire de point sur la grille de
% simulation. On crée un disque de la taille d'une doigt pour l'impact.
% Attention à ce que toute la source soit à l'intérieur du matériau simulé.
% Dans le cas présent, la source ne doit pas être dans un périmètre de 4dx
% du bord.

% position de la source à trouver dans le medium
sourcePosx = 6;         % min 4, max Mx-4
sourcePosy = 6;         % min 4, max Mx-4

sourceGrid = [sourcePosx + 3, sourcePosy + 3];

% Pour l'affichage, on transforme les points de la grille de simulation en
% position cartésienne. 
source_x_pos = kgrid.x_vec(sourceGrid(1));         % [grid points]
source_y_pos = kgrid.y_vec(sourceGrid(2));         % [grid points]

%% Visualisation de la grille de simulation
% On peut s'assurer que tous nos paramètres sont correctement défini à
% l'aide d'un graphique.

figure;
imagesc(kgrid.y_vec*1e3, kgrid.x_vec*1e3, medium.sound_speed); axis image
ylabel('y - position [mm]')
xlabel('x - position [mm]')
c = colorbar;
c.Label.String = 'Speed of sound';
hold on;
plot(sensor.mask(2,:)*1e3, sensor.mask(1,:)*1e3, 'r.')
plot(source_y_pos*1e3, source_x_pos*1e3, 'b+')
legend('Sensor', 'Source')

%% Simulation
% preparation du stockage du data d'entrainement
filename = sprintf('ncube_with_slit_%dx%d.mat', Mx, My);

training_data = cell(Mx, My);

% Check if file exists
if isfile(filename)
    % Load existing data
    load(filename, 'training_data');
else
    % Run training and save data
    for i = 1:Mx
        for j = 1:My
            sourceGrid = [i, j];
            if medium.sound_speed(sourceGrid(1), sourceGrid(2)) == airSpeed
                training_data{i, j} = NaN;
            else
                source_radius = floor(0.01/dx);         % [grid points] (Taille d'un doigt)
                source_magnitude = 10;                  % [Pa]
                source_1 = source_magnitude * makeDisc(Nx, Ny, sourceGrid(1), sourceGrid(2), source_radius);
    
                source.p0 = source_1;
                sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor,...
                    'PMLSize', 2, 'PMLInside', false, 'DataCast', 'single');
    
                training_data{i, j} = sensor_data / max(sensor_data);
            end
        end
    end

    % Save data
    save(filename, 'training_data');
end

source_response = training_data{sourcePosx, sourcePosy};

correlation_map = zeros(Mx, My);

for i = 1:Mx
    for j = 1:My
        sourceGrid = [i + 3, j + 3];
        if medium.sound_speed(sourceGrid(1), sourceGrid(2)) == airSpeed  
            continue
        else
            corr = xcorr(training_data{i,j}, source_response);
            correlation_map(i,j) = max(corr);
        end
    end
end

max_value = max(correlation_map(:));
correlation_map_norm = correlation_map / max_value;
%% Plot heatmap

figure;
imagesc(correlation_map_norm);   % Create heatmap of normalized correlation values
colormap('gray');                % Use grayscale colormap
colorbar;                        % Add colorbar to visualize the intensity
xlabel('X grid points');
ylabel('Y grid points');
title('Greyscale Heatmap of Normalized Correlation Coefficients');
axis image; 

%% Plot correlation

% Find the x-coordinate of the peak value (maximum correlation) in the map
[~, x_peak] = max(max(correlation_map_norm, [], 1));

% Extract the correlation data along the y-axis at this x-coordinate
y_correlation_profile = correlation_map_norm(:, x_peak);

%% Perform Gaussian curve fitting

% Define the y grid points for the correlation profile
y_grid_points = (1:My)';

% Perform Gaussian fit to the y_correlation_profile data
gaussFit = fit(y_grid_points, y_correlation_profile, 'gauss1');

%% Plot correlation profile with Gaussian fit

% Find the x-coordinate of the peak value (maximum correlation) in the map
[~, x_peak] = max(max(correlation_map_norm, [], 1));

% Extract the correlation data along the y-axis at this x-coordinate
y_correlation_profile = correlation_map_norm(:, x_peak);

%% Perform Gaussian curve fitting

% Define the y grid points for the correlation profile
y_grid_points = (1:My)';

% Perform Gaussian fit to the y_correlation_profile data
gaussFit = fit(y_grid_points, y_correlation_profile, 'gauss1');

%% Plot correlation profile with Gaussian fit

% Create a new figure for the profile and Gaussian fit
figure;

% Plot the original correlation profile data
plot(y_grid_points, y_correlation_profile, 'b-', 'LineWidth', 2);  % Original data
hold on;

% Plot the Gaussian fit by evaluating it manually at each y_grid_point
y_fit_values = gaussFit(y_grid_points);
plot(y_grid_points, y_fit_values, 'r--', 'LineWidth', 2);  % Gaussian fit

% Add labels, title, and legend
xlabel('Y grid points');
ylabel('Normalized correlation coefficient');
title(sprintf('Correlation profile at X = %d with Gaussian Fit', x_peak));
legend('Data', 'Gaussian Fit');
grid on;