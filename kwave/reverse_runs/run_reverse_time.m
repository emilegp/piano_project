%% Clear
clear all; clc

%% Paramétrisation
% pose de toutes les variables pour les différentes simulations

% Dimensions qui résultent en 64cm x 64cm
Nx = 401;    % 401
Ny = 401;    % 401
dx = 16e-4;  % 16e-4
dy = 16e-4;  % 16e-4

% Nx, Ny, dx, dy, med_id, shapeid, sensorid, sourceid
x = reverse_time_corr(Nx,Ny, dx, dy, 2, 1, 1, 2); 