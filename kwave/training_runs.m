%% Clear
clear all; clc

%% Paramétrisation
% pose de toutes les variables pour les différentes simulations

% Dimensions qui résultent en 64cm x 64cm
Nx = 20;
Ny = 20;
dx = 5e-3;
dy = 5e-3;

wood.SoundSpeed = 4000;
wood.Density = 700;
wood.sensorlocs = [10,7];
wood.trainrows = [13, 9];
wood.sourcelocs = [13,6; 13,10]; % 1er el doit etre dans trainingrows

% pour l'étude statistique
woodsourcelocs = [];
alu.SoundSpeed = 5100;
alu.Density = 2700;

plexi.SoundSpeed = 2750;
plexi.Density = 1180;

% label forme dans la signature de la fonction run

% 3 derniers chiffres : id shape, pt sensor, pt source
% run(Nx, Ny, dx, dy, wood, 4, 1, 2);
run(Nx, Ny, dx, dy, wood, 5, 1, 1);
