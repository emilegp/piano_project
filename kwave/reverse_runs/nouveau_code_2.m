%% Installation
% Afin d'installer k-wave, référez-vous  au site http://www.k-wave.org/installation.php
% Vous aurez besoin de vous créer un compte afin d'y accéder.
% Assurez-vous que que la toolbox k-wave se situe AU DESSUS de la liste des
% path de votre matlab puisqu'elle écrase des fonctions natives de Matlab.
% Pour cette même raison, il serait judicieux de la remettre au bas de
% cette liste à la fin du mandat. 

%% Clear
clear all; clc

%% Simulation grid parameter
Nx = 401;               % number of grid points in the x (row) direction
Ny = 401;               % number of grid points in the y (column) direction
dx = 16e-4;            % grid points spacing in the x direction [m]
dy = 16e-4;            % grid points spacing in the y direction [m]

kgrid = kWaveGrid(Nx, dx, Ny, dy);

SoundSpeed = 4000;      % Sound speed in the main material [m/s]
Density = 700;         % Density of the main material [kg/m^3]


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

% Pour modifier la geometrie on peut ajouter des conditions comme ici
% creer un trou dans la surface.

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
%% Define sensors on specific lines (excluding air)
clear sensor

% Définir les lignes spécifiques sur lesquelles placer les capteurs
sensor_line_1 = round(Nx-(Nx /5));  % Par exemple, au milieu du matériau
sensor_line_2 = round(Nx-(Nx /3));  % Une autre ligne plus près du bas (facultatif)

% Liste des positions des capteurs sur les lignes définies (hors air)
sensor_positions = [];
for j = 1:Ny
    % Ajouter les capteurs sur la première ligne uniquement là où la vitesse du son n'est pas celle de l'air
    if medium.sound_speed(sensor_line_1, j) ~= airSpeed
        sensor_positions = [sensor_positions; sensor_line_1, j];
    end
    % Ajouter les capteurs sur la deuxième ligne uniquement là où la vitesse du son n'est pas celle de l'air
    if medium.sound_speed(sensor_line_2, j) ~= airSpeed
        sensor_positions = [sensor_positions; sensor_line_2, j];
    end
end

% Convertir les indices de la grille en coordonnées cartésiennes
sensorXGrid = sensor_positions(:, 1);  % Coordonnées X des capteurs
sensorYGrid = sensor_positions(:, 2);  % Coordonnées Y des capteurs

% Le masque des capteurs doit être une matrice 2xN où N est le nombre de capteurs sur les lignes définies
sensor.mask = [kgrid.x_vec(sensorXGrid)'; kgrid.y_vec(sensorYGrid)'];


%% Source definition
% De même, la source est défini grâce à une paire de point sur la grille de
% simulation. On crée un disque de la taille d'une doigt pour l'impact.
% Attention à ce que toute la source soit à l'intérieur du matériau simulé.
% Dans le cas présent, la source ne doit pas être dans un périmètre de 4dx
% du bord.

sourceGrid = [220, 175];
source_radius = floor(0.01/dx);         % [grid points] (Taille d'un doigt)
source_magnitude = 10;                  % [Pa]
source_1 = source_magnitude*makeDisc(Nx, Ny, sourceGrid(1), sourceGrid(2), source_radius);

source.p0 = source_1;

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
% Pour accélérer la simulation, on réduit la taille du Perfectly Matching
% Layer (https://en.wikipedia.org/wiki/Perfectly_matched_layer).

sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor,...
    'PMLSize', 2, 'PMLInside', false, 'DataCast', 'single');


%% Sauvegarde des données
% Sauvegarder les données pour les réutiliser plus tard, où pour les
% exporter vers python. Pour load dans python, utiliser scipy.io.loadmat()

save('Sim1.mat', 'sensor_data')

%% Time-reversal of the sensor data
% Inverser les données capturées au niveau des capteurs dans le temps
sensor_data_reversed = flip(sensor_data, 2);  % Inverser selon la dimension temporelle
save("sensor_data_reversed.mat","sensor_data_reversed");
%% Define new source for time reversal
% La nouvelle source est définie par les données inversées du capteur
source.p = sensor_data_reversed;

% Le masque de la source doit correspondre à la position des capteurs
source.p_mask = sensor.mask;

% Initialisation d'une matrice pour stocker les données avec des zéros aux
% endroits où il n'y a pas de capteur
sensor_data_reversed_full = zeros(Nx, Ny, size(sensor_data_reversed, 2));

% Placer les données inversées aux positions des capteurs
for n = 1:size(sensor_positions, 1)
    i = sensor_positions(n, 1);  % Coordonnées X du capteur
    j = sensor_positions(n, 2);  % Coordonnées Y du capteur
    sensor_data_reversed_full(i, j, :) = sensor_data_reversed(n, :);
end

% Sauvegarde des données complètes avec des zéros
save("sensor_data_reversed_full.mat", "sensor_data_reversed_full");

% Paramètres de la simulation
[Nx, Ny, Nt] = size(sensor_data_reversed_full);  % Dimensions des données
dt = 5e-7;  % Intervalle de temps (en secondes)
t_array = (0:Nt-1) * dt * 1e6;  % Tableau de temps en microsecondes

% Préparation des données coupées
sensor_data_cut = zeros(Nx, Ny, Nt);  % Matrice pour les données coupées
lengths = zeros(Nx, Ny);  % Tableau pour stocker les longueurs coupées de chaque signal

% Appliquer la technique du max/20 pour chaque signal (en ignorant les zéros)
for i = 1:Nx
    for j = 1:Ny
        if all(sensor_data_reversed_full(i, j, :) == 0)
            % Ignorer les positions où il n'y a pas de signal (zéros partout)
            continue;
        end
        
        % Extraire le signal pour la position (i, j)
        sensor_signal = squeeze(sensor_data_reversed_full(i, j, :));
        
        % Trouver l'amplitude maximale en valeur absolue
        max_amplitude = max(abs(sensor_signal));
        threshold = max_amplitude / 20;  % Définir le seuil

        % Parcourir le signal à partir de la fin et couper dès que l'amplitude > threshold
        cut_index = Nt;
        for idx = Nt:-1:1
            if abs(sensor_signal(idx)) > threshold
                cut_index = idx;
                break;
            end
        end
        
        % Stocker la partie coupée du signal
        sensor_signal_cut = sensor_signal(1:cut_index);
        
        % Sauvegarder le signal coupé dans la matrice
        sensor_data_cut(i, j, 1:cut_index) = sensor_signal_cut;
        
        % Enregistrer la longueur du signal coupé
        lengths(i, j) = cut_index;
    end
end

% Trouver la longueur minimale parmi tous les signaux coupés
min_length = min(lengths(lengths > 0));  % Ignorer les longueurs de 0

% Ajuster tous les signaux à la longueur minimale en coupant le début
sensor_data_adjusted = zeros(Nx, Ny, min_length);  % Matrice pour les signaux ajustés
for i = 1:Nx
    for j = 1:Ny
        if all(sensor_data_reversed_full(i, j, :) == 0)
            % Ignorer les positions sans signal
            continue;
        end
        
        % Extraire le signal coupé
        sensor_signal_cut = squeeze(sensor_data_cut(i, j, :));
        sensor_signal_cut = sensor_signal_cut(1:lengths(i, j));  % Récupérer la partie utile

        % Si le signal est plus long que min_length, couper le début
        if lengths(i, j) > min_length
            start_index = lengths(i, j) - min_length + 1;
            sensor_signal_adjusted = sensor_signal_cut(start_index:end);
        else
            % Sinon, garder tout le signal coupé
            sensor_signal_adjusted = sensor_signal_cut;
        end
        
        % Sauvegarder le signal ajusté
        sensor_data_adjusted(i, j, :) = sensor_signal_adjusted;
    end
end

% Sauvegarder les signaux ajustés avec la même longueur
save("sensor_data_adjusted.mat", "sensor_data_adjusted");

% Graphique d'un signal ajusté
n = 400;  % Choisir un capteur
i = sensorXGrid(n);  % Coordonnée X
j = sensorYGrid(n);  % Coordonnée Y
sensor_signal_adjusted = squeeze(sensor_data_adjusted(i, j, :));  % Signal ajusté

% Tracer le signal ajusté
t_array_cut = t_array(1:min_length);  % Temps pour le signal ajusté
figure;
plot(t_array_cut, sensor_signal_adjusted);
xlabel('Temps[µs]');
ylabel('Amplitude');
title('Signal ajusté avec longueur uniforme');
grid on;

% Afficher la longueur du signal ajusté
disp(['La longueur du signal ajusté pour le capteur à la position (', num2str(i), ', ', num2str(j), ') est : ', num2str(length(sensor_signal_adjusted))]);
