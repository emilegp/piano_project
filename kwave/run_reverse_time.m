%% Clear
clear all; clc

%% Paramétrisation
% Pose de toutes les variables pour les différentes simulations

% Dimensions qui résultent en environ 60x60 cm
Nx = 196;
Ny = 196;
dx = 32e-4;
dy = 32e-4;

% Mémoire pour les résultats
results = {};

% for loop pour simuler toutes les combinaisons
for i = 1:2
    for j = 1:6
        for k = 1:3
            % parametres : Nx, Ny, dx, dy, med_id, shapeid, sensorid
            x = reverse_time_corr(Nx, Ny, dx, dy, i, j, k); 

            % ajout du résultat en mémoire
            results(end+1, :) = num2cell(x(:)');
        end
    end
end

% sauvegarde en csv
filename = 'simulation_results.csv';
writecell(results, filename);

fprintf('Results have been saved to %s\n', filename);