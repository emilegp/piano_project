function result = reverse_time_corr(Nx, Ny, dx, dy, med_id, shapeid, ...
    sensorid)

geo_data = geometry(Nx, Ny, dx, dy, shapeid, sensorid, med_id);

kgrid = kWaveGrid(Nx, dx, Ny, dy);

medium = gen_medium(geo_data);
airSpeed = 330;  
%% Placement des sensors pour retournement temporel
% les données de ces sensors deviennent des données de sources post flip

sensor_positions = [];
sensor_line_1 = round(Nx - (Nx / 5));  % Ligne de capteur 1

% Placer les sensors seulement sur les lignes spécifiées
for i = [sensor_line_1]
    for j = 1:Ny
        if medium.sound_speed(i, j) ~= airSpeed
            % Ajouter les positions de grille (i, j) aux capteurs
            sensor_positions = [sensor_positions; i, j];
        end
    end
end

% Convertir les indices de la grille en coordonnées cartésiennes
sensorXGrid = sensor_positions(:, 1);  % Coordonnées X des capteurs
sensorYGrid = sensor_positions(:, 2);  % Coordonnées Y des capteurs

% Le masque des capteurs doit être une matrice 2xN où N est le nombre de 
% capteurs sur le matériau
sensor.mask = [kgrid.x_vec(sensorXGrid)'; kgrid.y_vec(sensorYGrid)'];

%% Placement de la source

%un pt pour tester pour l'instant
source_loc = sensor_loc(geo_data);

sourceGrid = [source_loc(1), source_loc(2)];
source_radius = floor(0.01/dx);         % [grid points] (Taille d'un doigt)
source_magnitude = 10;                  % [Pa]
source_1 = source_magnitude*makeDisc(Nx, Ny, sourceGrid(1), sourceGrid(2), source_radius);

source.p0 = source_1;

% Pour l'affichage, on transforme les points de la grille de simulation en
% position cartésienne. 
source_x_pos = kgrid.x_vec(sourceGrid(1));         % [grid points]
source_y_pos = kgrid.y_vec(sourceGrid(2));         % [grid points]

%% Simulation
% Pour accélérer la simulation, on réduit la taille du Perfectly Matching
% Layer (https://en.wikipedia.org/wiki/Perfectly_matched_layer).
filename = "big_test.mat";
if isfile(filename)
    load(filename, "sensor_data_reversed");
else
    sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor,...
    'PMLSize', 2, 'PMLInside', false, 'DataCast', 'single');

    sensor_data_reversed = flip(sensor_data, 2);
    % La nouvelle source est définie par les données inversées du capteur
    source.p = sensor_data_reversed;
    save("sensor_data_reversed.mat","sensor_data_reversed");
end

%% Renversement temporel

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

%% Coupage des données avant l'onde ballistique
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

%% Ajustement des données pour avoir la meme longueur
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

%% For loop pour plusieurs points tests pour etude stats

sources = [sensor_line_1,60; sensor_line_1,75; sensor_line_1,90; 
    sensor_line_1,100; sensor_line_1,110; sensor_line_1,125; sensor_line_1,140];
num_sources = size(sources, 1); % Number of source points

contrast_list = [];
resolution_list = [];
for src_idx = 1:num_sources
    sourcex = sources(src_idx, 1);
    sourcey = sources(src_idx, 2);
    
    % Correlation
    source_response = squeeze(sensor_data_adjusted(sourcex, sourcey, :));
    correlation_map = zeros(Nx, Ny);
    
    for j = 1:Nx
        for k = 1:Ny % Changed from i to k to avoid conflict
            sourceGrid = [j, k];
            if medium.sound_speed(sourceGrid(1), sourceGrid(2)) == airSpeed  
                continue
            else
                corr = xcorr(squeeze(sensor_data_adjusted(j, k, :)), source_response);
                correlation_map(j, k) = max(corr);
            end
        end
    end
    
    corr_in_medium = correlation_map(4:Nx-4, 4:Ny-4);
    max_value = max(correlation_map(:));
    correlation_map_norm = corr_in_medium / max_value;

    %% Data along one line and gaussian fit
    correlation_line = correlation_map_norm(sourcex-3, :);
    
    % Prepare data for Gaussian fitting
    x_data = (4:Ny-4)';  % x data for fitting
    y_data = correlation_line';  % y data for fitting
    
    % Define the Gaussian model with an offset
    gaussian_model = fittype('A*exp(-((x-mu)^2)/(2*sigma^2)) + C', ...
                             'independent', 'x', ...
                             'coefficients', {'A', 'mu', 'sigma', 'C'});
    
    % Initial guesses for the fit parameters
    initial_guess = [max(y_data), mean(x_data), std(x_data), min(y_data)]; % [A, mu, sigma, C]
    
    % Fit the model to the data
    [fit_result, gof] = fit(x_data, y_data, gaussian_model, 'StartPoint', initial_guess);
    
    % Generate fitted values for smooth curve
    x_fit = linspace(min(x_data), max(x_data), 100);
    y_fit = feval(fit_result, x_fit);
    
    if src_idx == 1
        %% Plotting the First Two Heatmaps Side by Side
        fig1 = figure('Position', [100, 100, 1000, 700]);
        
        % Left subplot for the first heatmap
        subplot(1, 2, 1); % 1 row, 2 columns, first subplot
        % set(gca, 'YDir', 'normal');
        imagesc(kgrid.y_vec * 1e3, kgrid.x_vec * 1e3, medium.sound_speed); 
        axis image;
        xlabel('Position en x [mm]');
        ylabel('Position en y [mm]');
        c1 = colorbar;
        c1.Label.String = "Vitesse du son";
        hold on;
        plot(sensor.mask(2, :) * 1e3, sensor.mask(1, :) * 1e3, 'r.');
        plot(source_y_pos * 1e3, source_x_pos * 1e3, 'b+');
        title('Visualisation de la géométrie');
        legend('Capteur', 'Source');
        hold off;
        
        % Right subplot for the second heatmap (Correlation Map)
        subplot(1, 2, 2); % 1 row, 2 columns, second subplot
        imagesc(correlation_map_norm);
        axis image;
        
        % Set the x-ticks based on pixel counts multiplied by dx and converted to mm
        x_ticks = get(gca, 'XTick');  % Get current X tick positions
        y_ticks = get(gca, 'YTick');  % Get current Y tick positions
        set(gca, 'XTickLabel', x_ticks * dx * 10^3);  % Convert X tick labels to mm
        
        % Adjust Y tick labels to start from the bottom
        y_tick_labels = flip(y_ticks * dx * 10^3);  % Flip and convert Y tick labels to mm
        set(gca, 'YTickLabel', y_tick_labels);  % Set new Y tick labels
        
        % Add axis labels
        xlabel('Position en x [mm]');
        ylabel('Position en y [mm]');
        c2 = colorbar;
        title(sprintf('Carte des coefficients\n de corrélation'));

        saveas(fig1, "heatmaps_big_test.png")
        
        % Create a new figure for the Gaussian fit
        fig2 = figure;
        
        % Align x_data to start from 0
        x_data_adjusted = x_data - x_data(1);
        plot(x_data_adjusted * dy * 10^3, y_data, 'ro', 'MarkerFaceColor', 'r');  % Original data points
        hold on;
        
        % Adjust x_fit similarly
        x_fit_adjusted = x_fit - x_data(1);
        x_fit_mm = x_fit_adjusted * dy * 10^3;
        plot(x_fit_mm, y_fit, 'b-', 'LineWidth', 2); % Blue line for the fit
        
        % Set x-axis limits to start at 0
        xlim([0 max(x_fit_mm)]);  % Start x-axis from 0
        
        % Set custom ticks every 100 units, starting from 0
        xticks = 0:100:max(x_fit_mm); % Ticks every 100
        set(gca, 'XTick', xticks, 'XTickLabel', xticks);
        
        xlabel("Position selon l'axe des X")
        ylabel('Coefficient de corrélation')
        title(sprintf(["Gaussienne ajustée aux coefficients de corrélation entre\n une source et les données d'entrainement"]))
        legend('Coefficients', 'Gaussienne ajustée');
        grid on;
        hold off;

        saveas(fig2, "gaussian_big_test.png")



    end
    
    % Display the fitted parameters
    disp(fit_result);
    
    % Access individual parameters
    A_fitted = fit_result.A;
    mu_fitted = fit_result.mu;
    sigma_fitted = fit_result.sigma;
    C_fitted = fit_result.C;
    
    % Optionally, print the fitted parameters
    fprintf('Fitted parameters: A = %.4f, mu = %.4f, sigma = %.4f, C = %.4f\n', ...
            A_fitted, mu_fitted, sigma_fitted, C_fitted);

    contrast = 1-C_fitted;
    fprintf('Contrast = %.4f\n', contrast);

    FWHM = 2 * sqrt(2 * log(2)) * sigma_fitted;

    % Optionally, print the FWHM
    fprintf('Full Width at Half Maximum (FWHM) = %.4f\n', FWHM);
    
    contrast_list = [contrast_list, contrast];
    resolution_list = [resolution_list, FWHM];
end


mean_contrast = mean(contrast_list);
std_contrast = std(contrast_list);

% Display result as x ± delta x
fprintf('Contrast = %.4f ± %.4f\n', mean_contrast, std_contrast);

mean_res = mean(resolution_list);
std_res = std(resolution_list);

% Display result as x ± delta x
fprintf('Resolution = %.4f ± %.4f\n', mean_res, std_res);

sim = sprintf("mat%d_geo%d_sensor%d", med_id, shapeid, sensorid);
result = [sim, mean_contrast, std_contrast, mean_res, std_res];

end
