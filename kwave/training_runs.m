%% Clear
clear all; clc

%% Paramétrisation
% pose de toutes les variables pour les différentes simulations

% Dimensions qui résultent en 64cm x 64cm
Nx = 32;
Ny = 32;
dx = 2e-2;
dy = 2e-2;

wood.SoundSpeed = 4000;
wood.Density = 700;
wood.sensorlocs = [8,16; 16,16; 19,10; 9,13; 20,12; 20,20]; % doit être entre 4 et N-4
wood.trainrows = [23, 27];
wood.sourcelocs = [23,8 ; 23,15; 23,25; 27,8; 27,15; 27,25; 23,12 ; 23,18; 
    23,24; 27,12; 27,18; 27,24]; % 1er el doit etre dans trainingrows

% pour l'étude statistique
woodsourcelocs = [];
alu.SoundSpeed = 5100;
alu.Density = 2700;

plexi.SoundSpeed = 2750;
plexi.Density = 1180;

% 3 derniers chiffres : id shape, pt sensor, pt source
% run(Nx, Ny, dx, dy, wood, 4, 1, 2);


% shape 1 : 
% sensor (8,16; 16,16; 19,10)
% source (23,8 ; 23,15; 23,25; 27,8; 27,15; 27,25)
% rows 23, 27
run(Nx, Ny, dx, dy, wood, 1, 1, 1);
run(Nx, Ny, dx, dy, wood, 1, 1, 2);
run(Nx, Ny, dx, dy, wood, 1, 1, 3);
run(Nx, Ny, dx, dy, wood, 1, 1, 4);
run(Nx, Ny, dx, dy, wood, 1, 1, 5);
run(Nx, Ny, dx, dy, wood, 1, 1, 6);
run(Nx, Ny, dx, dy, wood, 1, 2, 1);
run(Nx, Ny, dx, dy, wood, 1, 2, 2);
run(Nx, Ny, dx, dy, wood, 1, 2, 3);
run(Nx, Ny, dx, dy, wood, 1, 2, 4);
run(Nx, Ny, dx, dy, wood, 1, 2, 5);
run(Nx, Ny, dx, dy, wood, 1, 2, 6);
run(Nx, Ny, dx, dy, wood, 1, 3, 1);
run(Nx, Ny, dx, dy, wood, 1, 3, 2);
run(Nx, Ny, dx, dy, wood, 1, 3, 3);
run(Nx, Ny, dx, dy, wood, 1, 3, 4);
run(Nx, Ny, dx, dy, wood, 1, 3, 5);
run(Nx, Ny, dx, dy, wood, 1, 3, 6);


% shape 2 : idem shape 1
run(Nx, Ny, dx, dy, wood, 2, 1, 1);
run(Nx, Ny, dx, dy, wood, 2, 1, 2);
run(Nx, Ny, dx, dy, wood, 2, 1, 3);
run(Nx, Ny, dx, dy, wood, 2, 1, 4);
run(Nx, Ny, dx, dy, wood, 2, 1, 5);
run(Nx, Ny, dx, dy, wood, 2, 1, 6);
run(Nx, Ny, dx, dy, wood, 2, 2, 1);
run(Nx, Ny, dx, dy, wood, 2, 2, 2);
run(Nx, Ny, dx, dy, wood, 2, 2, 3);
run(Nx, Ny, dx, dy, wood, 2, 2, 4);
run(Nx, Ny, dx, dy, wood, 2, 2, 5);
run(Nx, Ny, dx, dy, wood, 2, 2, 6);
run(Nx, Ny, dx, dy, wood, 2, 3, 1);
run(Nx, Ny, dx, dy, wood, 2, 3, 2);
run(Nx, Ny, dx, dy, wood, 2, 3, 3);
run(Nx, Ny, dx, dy, wood, 2, 3, 4);
run(Nx, Ny, dx, dy, wood, 2, 3, 5);
run(Nx, Ny, dx, dy, wood, 2, 3, 6);

% shape 3 :
% sensor (9,13; 16,16; 19,10)
% source (23,8 ; 23,15; 23,25; 27,8; 27,15; 27,25)
% rows 23, 27
run(Nx, Ny, dx, dy, wood, 3, 1, 1);
run(Nx, Ny, dx, dy, wood, 3, 1, 2);
run(Nx, Ny, dx, dy, wood, 3, 1, 3);
run(Nx, Ny, dx, dy, wood, 3, 1, 4);
run(Nx, Ny, dx, dy, wood, 3, 1, 5);
run(Nx, Ny, dx, dy, wood, 3, 1, 6);
run(Nx, Ny, dx, dy, wood, 3, 2, 1);
run(Nx, Ny, dx, dy, wood, 3, 2, 2);
run(Nx, Ny, dx, dy, wood, 3, 2, 3);
run(Nx, Ny, dx, dy, wood, 3, 2, 4);
run(Nx, Ny, dx, dy, wood, 3, 2, 5);
run(Nx, Ny, dx, dy, wood, 3, 2, 6);
run(Nx, Ny, dx, dy, wood, 3, 4, 1);
run(Nx, Ny, dx, dy, wood, 3, 4, 2);
run(Nx, Ny, dx, dy, wood, 3, 4, 3);
run(Nx, Ny, dx, dy, wood, 3, 4, 4);
run(Nx, Ny, dx, dy, wood, 3, 4, 5);
run(Nx, Ny, dx, dy, wood, 3, 4, 6);

% shape 4 : idem shape 1
% too bad

% shape 5 :
% sensor (9,13; 16,16; 19,10)
% source (23,12 ; 23,18; 23,24; 27,12; 27,18; 27,24)
% rows 23, 27
run(Nx, Ny, dx, dy, wood, 5, 1, 7);
run(Nx, Ny, dx, dy, wood, 5, 1, 8);
run(Nx, Ny, dx, dy, wood, 5, 1, 9);
run(Nx, Ny, dx, dy, wood, 5, 1, 10);
run(Nx, Ny, dx, dy, wood, 5, 1, 11);
run(Nx, Ny, dx, dy, wood, 5, 1, 12);
run(Nx, Ny, dx, dy, wood, 5, 2, 7);
run(Nx, Ny, dx, dy, wood, 5, 2, 8);
run(Nx, Ny, dx, dy, wood, 5, 2, 9);
run(Nx, Ny, dx, dy, wood, 5, 2, 10);
run(Nx, Ny, dx, dy, wood, 5, 2, 11);
run(Nx, Ny, dx, dy, wood, 5, 2, 12);
run(Nx, Ny, dx, dy, wood, 5, 4, 7);
run(Nx, Ny, dx, dy, wood, 5, 4, 8);
run(Nx, Ny, dx, dy, wood, 5, 4, 9);
run(Nx, Ny, dx, dy, wood, 5, 4, 10);
run(Nx, Ny, dx, dy, wood, 5, 4, 11);
run(Nx, Ny, dx, dy, wood, 5, 4, 12);

% shape 6 : 
% sensor (20,12; 20,20)
% source (23,12 ; 23,18; 23,25; 27,8; 27,15; 27,25)
% rows 23, 27
run(Nx, Ny, dx, dy, wood, 6, 5, 1);
run(Nx, Ny, dx, dy, wood, 6, 5, 2);
run(Nx, Ny, dx, dy, wood, 6, 5, 3);
run(Nx, Ny, dx, dy, wood, 6, 5, 4);
run(Nx, Ny, dx, dy, wood, 6, 5, 5);
run(Nx, Ny, dx, dy, wood, 6, 5, 6);
run(Nx, Ny, dx, dy, wood, 6, 6, 1);
run(Nx, Ny, dx, dy, wood, 6, 6, 2);
run(Nx, Ny, dx, dy, wood, 6, 6, 3);
run(Nx, Ny, dx, dy, wood, 6, 6, 4);
run(Nx, Ny, dx, dy, wood, 6, 6, 5);
run(Nx, Ny, dx, dy, wood, 6, 6, 6);


%repeat 3 materiaux

run(Nx, Ny, dx, dy, alu, 1, 1, 1);
run(Nx, Ny, dx, dy, alu, 1, 1, 2);
run(Nx, Ny, dx, dy, alu, 1, 1, 3);
run(Nx, Ny, dx, dy, alu, 1, 1, 4);
run(Nx, Ny, dx, dy, alu, 1, 1, 5);
run(Nx, Ny, dx, dy, alu, 1, 1, 6);
run(Nx, Ny, dx, dy, alu, 1, 2, 1);
run(Nx, Ny, dx, dy, alu, 1, 2, 2);
run(Nx, Ny, dx, dy, alu, 1, 2, 3);
run(Nx, Ny, dx, dy, alu, 1, 2, 4);
run(Nx, Ny, dx, dy, alu, 1, 2, 5);
run(Nx, Ny, dx, dy, alu, 1, 2, 6);
run(Nx, Ny, dx, dy, alu, 1, 3, 1);
run(Nx, Ny, dx, dy, alu, 1, 3, 2);
run(Nx, Ny, dx, dy, alu, 1, 3, 3);
run(Nx, Ny, dx, dy, alu, 1, 3, 4);
run(Nx, Ny, dx, dy, alu, 1, 3, 5);
run(Nx, Ny, dx, dy, alu, 1, 3, 6);

% shape 2 : idem shape 1
run(Nx, Ny, dx, dy, alu, 2, 1, 1);
run(Nx, Ny, dx, dy, alu, 2, 1, 2);
run(Nx, Ny, dx, dy, alu, 2, 1, 3);
run(Nx, Ny, dx, dy, alu, 2, 1, 4);
run(Nx, Ny, dx, dy, alu, 2, 1, 5);
run(Nx, Ny, dx, dy, alu, 2, 1, 6);
run(Nx, Ny, dx, dy, alu, 2, 2, 1);
run(Nx, Ny, dx, dy, alu, 2, 2, 2);
run(Nx, Ny, dx, dy, alu, 2, 2, 3);
run(Nx, Ny, dx, dy, alu, 2, 2, 4);
run(Nx, Ny, dx, dy, alu, 2, 2, 5);
run(Nx, Ny, dx, dy, alu, 2, 2, 6);
run(Nx, Ny, dx, dy, alu, 2, 3, 1);
run(Nx, Ny, dx, dy, alu, 2, 3, 2);
run(Nx, Ny, dx, dy, alu, 2, 3, 3);
run(Nx, Ny, dx, dy, alu, 2, 3, 4);
run(Nx, Ny, dx, dy, alu, 2, 3, 5);
run(Nx, Ny, dx, dy, alu, 2, 3, 6);

% shape 3 :
% sensor (9,13; 16,16; 19,10)
% source (23,8 ; 23,15; 23,25; 27,8; 27,15; 27,25)
% rows 23, 27
run(Nx, Ny, dx, dy, alu, 3, 1, 1);
run(Nx, Ny, dx, dy, alu, 3, 1, 2);
run(Nx, Ny, dx, dy, alu, 3, 1, 3);
run(Nx, Ny, dx, dy, alu, 3, 1, 4);
run(Nx, Ny, dx, dy, alu, 3, 1, 5);
run(Nx, Ny, dx, dy, alu, 3, 1, 6);
run(Nx, Ny, dx, dy, alu, 3, 2, 1);
run(Nx, Ny, dx, dy, alu, 3, 2, 2);
run(Nx, Ny, dx, dy, alu, 3, 2, 3);
run(Nx, Ny, dx, dy, alu, 3, 2, 4);
run(Nx, Ny, dx, dy, alu, 3, 2, 5);
run(Nx, Ny, dx, dy, alu, 3, 2, 6);
run(Nx, Ny, dx, dy, alu, 3, 4, 1);
run(Nx, Ny, dx, dy, alu, 3, 4, 2);
run(Nx, Ny, dx, dy, alu, 3, 4, 3);
run(Nx, Ny, dx, dy, alu, 3, 4, 4);
run(Nx, Ny, dx, dy, alu, 3, 4, 5);
run(Nx, Ny, dx, dy, alu, 3, 4, 6);

% shape 4 : idem shape 1
% too bad

% shape 5 :
% sensor (9,13; 16,16; 19,10)
% source (23,12 ; 23,18; 23,24; 27,12; 27,18; 27,24)
% rows 23, 27
run(Nx, Ny, dx, dy, alu, 5, 1, 7);
run(Nx, Ny, dx, dy, alu, 5, 1, 8);
run(Nx, Ny, dx, dy, alu, 5, 1, 9);
run(Nx, Ny, dx, dy, alu, 5, 1, 10);
run(Nx, Ny, dx, dy, alu, 5, 1, 11);
run(Nx, Ny, dx, dy, alu, 5, 1, 12);
run(Nx, Ny, dx, dy, alu, 5, 2, 7);
run(Nx, Ny, dx, dy, alu, 5, 2, 8);
run(Nx, Ny, dx, dy, alu, 5, 2, 9);
run(Nx, Ny, dx, dy, alu, 5, 2, 10);
run(Nx, Ny, dx, dy, alu, 5, 2, 11);
run(Nx, Ny, dx, dy, alu, 5, 2, 12);
run(Nx, Ny, dx, dy, alu, 5, 4, 7);
run(Nx, Ny, dx, dy, alu, 5, 4, 8);
run(Nx, Ny, dx, dy, alu, 5, 4, 9);
run(Nx, Ny, dx, dy, alu, 5, 4, 10);
run(Nx, Ny, dx, dy, alu, 5, 4, 11);
run(Nx, Ny, dx, dy, alu, 5, 4, 12);

% shape 6 : 
% sensor (20,12; 20,20)
% source (23,12 ; 23,18; 23,25; 27,8; 27,15; 27,25)
% rows 23, 27
run(Nx, Ny, dx, dy, alu, 6, 5, 1);
run(Nx, Ny, dx, dy, alu, 6, 5, 2);
run(Nx, Ny, dx, dy, alu, 6, 5, 3);
run(Nx, Ny, dx, dy, alu, 6, 5, 4);
run(Nx, Ny, dx, dy, alu, 6, 5, 5);
run(Nx, Ny, dx, dy, alu, 6, 5, 6);
run(Nx, Ny, dx, dy, alu, 6, 6, 1);
run(Nx, Ny, dx, dy, alu, 6, 6, 2);
run(Nx, Ny, dx, dy, alu, 6, 6, 3);
run(Nx, Ny, dx, dy, alu, 6, 6, 4);
run(Nx, Ny, dx, dy, alu, 6, 6, 5);
run(Nx, Ny, dx, dy, alu, 6, 6, 6);

% shape 1
run(Nx, Ny, dx, dy, plexi, 1, 1, 1);
run(Nx, Ny, dx, dy, plexi, 1, 1, 2);
run(Nx, Ny, dx, dy, plexi, 1, 1, 3);
run(Nx, Ny, dx, dy, plexi, 1, 1, 4);
run(Nx, Ny, dx, dy, plexi, 1, 1, 5);
run(Nx, Ny, dx, dy, plexi, 1, 1, 6);
run(Nx, Ny, dx, dy, plexi, 1, 2, 1);
run(Nx, Ny, dx, dy, plexi, 1, 2, 2);
run(Nx, Ny, dx, dy, plexi, 1, 2, 3);
run(Nx, Ny, dx, dy, plexi, 1, 2, 4);
run(Nx, Ny, dx, dy, plexi, 1, 2, 5);
run(Nx, Ny, dx, dy, plexi, 1, 2, 6);
run(Nx, Ny, dx, dy, plexi, 1, 3, 1);
run(Nx, Ny, dx, dy, plexi, 1, 3, 2);
run(Nx, Ny, dx, dy, plexi, 1, 3, 3);
run(Nx, Ny, dx, dy, plexi, 1, 3, 4);
run(Nx, Ny, dx, dy, plexi, 1, 3, 5);
run(Nx, Ny, dx, dy, plexi, 1, 3, 6);

% shape 2 : idem shape 1
run(Nx, Ny, dx, dy, plexi, 2, 1, 1);
run(Nx, Ny, dx, dy, plexi, 2, 1, 2);
run(Nx, Ny, dx, dy, plexi, 2, 1, 3);
run(Nx, Ny, dx, dy, plexi, 2, 1, 4);
run(Nx, Ny, dx, dy, plexi, 2, 1, 5);
run(Nx, Ny, dx, dy, plexi, 2, 1, 6);
run(Nx, Ny, dx, dy, plexi, 2, 2, 1);
run(Nx, Ny, dx, dy, plexi, 2, 2, 2);
run(Nx, Ny, dx, dy, plexi, 2, 2, 3);
run(Nx, Ny, dx, dy, plexi, 2, 2, 4);
run(Nx, Ny, dx, dy, plexi, 2, 2, 5);
run(Nx, Ny, dx, dy, plexi, 2, 2, 6);
run(Nx, Ny, dx, dy, plexi, 2, 3, 1);
run(Nx, Ny, dx, dy, plexi, 2, 3, 2);
run(Nx, Ny, dx, dy, plexi, 2, 3, 3);
run(Nx, Ny, dx, dy, plexi, 2, 3, 4);
run(Nx, Ny, dx, dy, plexi, 2, 3, 5);
run(Nx, Ny, dx, dy, plexi, 2, 3, 6);

% shape 3
run(Nx, Ny, dx, dy, plexi, 3, 1, 1);
run(Nx, Ny, dx, dy, plexi, 3, 1, 2);
run(Nx, Ny, dx, dy, plexi, 3, 1, 3);
run(Nx, Ny, dx, dy, plexi, 3, 1, 4);
run(Nx, Ny, dx, dy, plexi, 3, 1, 5);
run(Nx, Ny, dx, dy, plexi, 3, 1, 6);
run(Nx, Ny, dx, dy, plexi, 3, 2, 1);
run(Nx, Ny, dx, dy, plexi, 3, 2, 2);
run(Nx, Ny, dx, dy, plexi, 3, 2, 3);
run(Nx, Ny, dx, dy, plexi, 3, 2, 4);
run(Nx, Ny, dx, dy, plexi, 3, 2, 5);
run(Nx, Ny, dx, dy, plexi, 3, 2, 6);
run(Nx, Ny, dx, dy, plexi, 3, 4, 1);
run(Nx, Ny, dx, dy, plexi, 3, 4, 2);
run(Nx, Ny, dx, dy, plexi, 3, 4, 3);
run(Nx, Ny, dx, dy, plexi, 3, 4, 4);
run(Nx, Ny, dx, dy, plexi, 3, 4, 5);
run(Nx, Ny, dx, dy, plexi, 3, 4, 6);

% shape 5
run(Nx, Ny, dx, dy, plexi, 5, 1, 7);
run(Nx, Ny, dx, dy, plexi, 5, 1, 8);
run(Nx, Ny, dx, dy, plexi, 5, 1, 9);
run(Nx, Ny, dx, dy, plexi, 5, 1, 10);
run(Nx, Ny, dx, dy, plexi, 5, 1, 11);
run(Nx, Ny, dx, dy, plexi, 5, 1, 12);
run(Nx, Ny, dx, dy, plexi, 5, 2, 7);
run(Nx, Ny, dx, dy, plexi, 5, 2, 8);
run(Nx, Ny, dx, dy, plexi, 5, 2, 9);
run(Nx, Ny, dx, dy, plexi, 5, 2, 10);
run(Nx, Ny, dx, dy, plexi, 5, 2, 11);
run(Nx, Ny, dx, dy, plexi, 5, 2, 12);
run(Nx, Ny, dx, dy, plexi, 5, 4, 7);
run(Nx, Ny, dx, dy, plexi, 5, 4, 8);
run(Nx, Ny, dx, dy, plexi, 5, 4, 9);
run(Nx, Ny, dx, dy, plexi, 5, 4, 10);
run(Nx, Ny, dx, dy, plexi, 5, 4, 11);
run(Nx, Ny, dx, dy, plexi, 5, 4, 12);

% shape 6
run(Nx, Ny, dx, dy, plexi, 6, 5, 1);
run(Nx, Ny, dx, dy, plexi, 6, 5, 2);
run(Nx, Ny, dx, dy, plexi, 6, 5, 3);
run(Nx, Ny, dx, dy, plexi, 6, 5, 4);
run(Nx, Ny, dx, dy, plexi, 6, 5, 5);
run(Nx, Ny, dx, dy, plexi, 6, 5, 6);
run(Nx, Ny, dx, dy, plexi, 6, 6, 1);
run(Nx, Ny, dx, dy, plexi, 6, 6, 2);
run(Nx, Ny, dx, dy, plexi, 6, 6, 3);
run(Nx, Ny, dx, dy, plexi, 6, 6, 4);
run(Nx, Ny, dx, dy, plexi, 6, 6, 5);
run(Nx, Ny, dx, dy, plexi, 6, 6, 6);
