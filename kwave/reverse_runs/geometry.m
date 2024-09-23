classdef geometry
    % proprietes geometriques et physique du materiau
    
    properties
        dimensions  % Nx Ny
        scale       % dx dy
        shape_id
        sensor_id
        source_id
        material_id
    end
    
    methods
        function obj = geometry(Nx, Ny, dx, dy, shapeID, sensorID, sourceID, ...
                materialID)
            % constructeur de la geometrie

            obj.dimensions = [Nx, Ny];
            obj.scale = [dx, dy];
            obj.shape_id = shapeID;
            obj.sensor_id = sensorID;
            obj.source_id = sourceID;
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
            if obj.material_id == 1 % bois
                med.soundSpeed = 4000;
                med.Density = 700;

            elseif obj.material_id== 2 % aluminium
                med.soundSpeed = 5100;
                med.Density = 2700;

            elseif obj.material_id == 3 % plexiglass
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
                        if i > 30 && i < 50 && j >= (Ny/5) && j <= (Ny/3)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 30 && i < 150 && j >= (Ny - (Ny/4)) && j <= (Ny - (Ny/1000))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 360 && i < 400 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 360 && i < 400 && j >= (Ny/4) && j <= (Ny/3)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif  j >= (300+i/1.2)
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
                        if j <= (200 - i/1.5) || j >= (200 + i/1.5)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 100 && i < 130 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 200 && i < 240 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        end
                    end
                end
            elseif obj.shape_id == 3
                for i = 1:Nx
                    for j = 1:Ny
                        if i > 100 && i < 130 && j >= (Ny - (Ny/2)) && j <= (Ny - (Ny/2.5))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 200 && i < 240 && j >= (Ny - (Ny/3)) && j <= (Ny - (Ny/4))
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif i > 100 && i < 180 && j >= (Ny/5) && j <= (Ny/3)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                        elseif j >= (300+i/1.2)
                            medium.sound_speed(i,j) = airSpeed;
                            medium.density(i,j) = airDensity;
                      
                        end
                    end
                end
            % shape == 4 ou autre résulte en un carré plein, test de symétrie

            % shape == 5 semble redondante, pas de pts trouvés pour elle
            % elseif obj.shape_id == 5
            %     for i = 1:Nx
            %         for j = 1:Ny 
            %             if (i - (Nx - 14.5))^2 + (j - (Ny - 14.5))^2 > 14.5^2 
            %                 medium.sound_speed(i,j) = airSpeed; 
            %                 medium.density(i,j) = airDensity;    
            %             end
            %         end
            %     end
            elseif obj.shape_id == 6
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
            end
            
            % return
            med_final = medium;

        end

        % function med = gen_medium_no_mat(obj, sound_speed, density)
        % 
        % 
        % end

        % ne retourne qu'un point
        function locs = sensor_loc(obj)
            if obj.shape_id == 1
                sensor_list = [100,100; 200,350; 30,200];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 2
                sensor_list = [80,200; 200,200; 250,80];
                locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 3
                sensor_list = [50,100; 200,370; 100,300];
                locs = sensor_list(obj.sensor_id, :);

            % elseif obj.shape_id == 4
            %     sensor_list = [80,200; 200,200; 250,80];
            %     locs = sensor_list(obj.sensor_id, :);


            % TEMP
            elseif obj.shape_id == 4
                sensor_list = [6,6; 7,8];
                locs = sensor_list(obj.sensor_id, :);


            % elseif obj.shape_id == 5
            %     sensor_list = [6,6; 7,8];
            %     locs = sensor_list(obj.sensor_id, :);

            elseif obj.shape_id == 6
                sensor_list = [300,300; 200,100; 220,175];
                locs = sensor_list(obj.sensor_id, :);
            else
                error('ID materiau invalide')
            end
        end

        % retourne une liste de pts pour l'étude statistique
        function locs = source_locs(obj)
            if obj.shape_id == 1
                locs = [100,100; 200,350; 30,200];

            elseif obj.shape_id == 2
                locs = [80,200; 200,200; 250,80];

            elseif obj.shape_id == 3
                locs = [50,100; 200,370; 100,300];

            elseif obj.shape_id == 4
                locs = [6,6; 7,8];

            elseif obj.shape_id == 5
                locs = [6,6; 7,8];

            elseif obj.shape_id == 6
                locs = [6,6; 7,8];

            else
                error('ID materiau invalide')
            end
        end
    end
end

