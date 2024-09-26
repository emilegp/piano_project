classdef geometry
    % proprietes geometriques et physique du materiau
    
    properties
        dimensions  % Nx Ny
        scale       % dx dy
        shape_id
        sensor_id
        material_id
    end
    
    methods
        function obj = geometry(Nx, Ny, dx, dy, shapeID, sensorID, ...
                materialID)
            % constructeur de la geometrie

            obj.dimensions = [Nx, Ny];
            obj.scale = [dx, dy];
            obj.shape_id = shapeID;
            obj.sensor_id = sensorID;
            obj.material_id = materialID;
        end
        
        function med_final = gen_medium(obj)
            dims = obj.dimensions;
            Nx = dims(1);
            Ny = dims(2);

            % genere un medium avec geometrie et materiau specifique
            airSpeed = 330;     % [m/s]
            airDensity = 10;    % [kg/m^3]    

            medium.alpha_coeff = 0.75;
            medium.alpha_power = 1.5;
            
            % materiau
            if obj.material_id == 1 % alu
                med.soundSpeed = 5100;
                med.Density = 2700;

            elseif obj.material_id== 2 % plexi
                med.soundSpeed = 2750;
                med.Density = 1180;

            else
                error('ID materiau invalide')
            end

            % geometrie
            medium.sound_speed = med.soundSpeed * ones(Nx, Ny); % Change SoundSpeed to sound_speed
            medium.density = med.Density * ones(Nx, Ny); % Change Density to density
            
            % air autour du materiau
            for i = 1:Nx
                for j = 1:Ny
                    if i < 4 || i > (Nx-4) || j < 4 || j > (Ny-4)
                        medium.sound_speed(i,j) = airSpeed;
                        medium.density(i,j) = airDensity;
                    end
                end
            end

            if obj.shape_id == 1
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
            elseif obj.shape_id == 2
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
            elseif obj.shape_id == 3
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
            % shape == 4 ou autre résulte en un carré plein, test de symétrie

            % shape == 5 semble redondante, pas de pts trouvés pour elle
            elseif obj.shape_id == 5
                for i = 1:Nx
                    for j = 1:Ny 
                        if (i - (Nx - 50))^2 + (j - (Ny - 50))^2 > 150^2 
                            medium.sound_speed(i,j) = airSpeed; 
                            medium.density(i,j) = airDensity;   
                   elseif i > 40 && i < 90 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/3))
                            medium.sound_speed(i,j) = airSpeed;
                   elseif  i > 40 && i < 90 && j >= (Ny/3) && j <= (Ny/2)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                   elseif i > 100 && i < 110 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                   elseif i > 90 && i < 95 && j >= (Ny - (Ny/6)) && j <= (Ny - (Ny/10))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        end
                    end
                end
            elseif obj.shape_id == 6
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
            end
            
            % return
            med_final = medium;

        end

        % liste des sensors par geometrie
        function locs = sensor_loc(obj)
            if obj.shape_id == 1
                sensor_list = [100,100; 50,100; 50,25];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 2
                sensor_list = [100,50; 25,100; 110,150];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 3
                sensor_list = [80,150; 20,100; 100,30];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 4
                sensor_list = [80,100; 100,100; 100,80];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 5
                sensor_list = [110,100; 30,100; 110,170];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 6
                sensor_list = [100,30; 100,180; 180,100];
                locs = sensor_list(obj.sensor_id, :);
            else
                error('ID materiau invalide')
            end
        end
    end
end

