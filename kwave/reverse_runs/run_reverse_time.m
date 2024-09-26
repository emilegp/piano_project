1%% Clear
clear all; clc

%% Paramétrisation
% Pose de toutes les variables pour les différentes simulations

% Dimensions qui résultent en 64cm x 64cm
Nx = 196;    % 196
Ny = 196;    % 196
dx = 32e-4;  % 32e-4
dy = 32e-4;  % 32e-4

% Initialize an empty cell array to store results
results = {};

% Nx, Ny, dx, dy, med_id, shapeid, sensorid
for i = 1:2
    for j = 1:6
        for k = 1:3
            % Run the function and store the result in 'x'
            x = reverse_time_corr(Nx, Ny, dx, dy, i, j, k); 

            % Flatten and append the result to the 'results' cell array
            results(end+1, :) = num2cell(x(:)');  % Store as a new row (non-nested)
        end
    end
end

% Export the results array to a file (e.g., CSV)
filename = 'simulation_results.csv';
writecell(results, filename);

fprintf('Results have been saved to %s\n', filename);