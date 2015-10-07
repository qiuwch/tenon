function lsp_convert_format(origDir)
    % Crop the image, to make it suitable for LSP format
    % Convert rendered images to blender format, crop images and save annotations to mat file
    cropDir = [origDir '/crop/'];
    numFiles = dir([origDir '/imgs/*.png']);

    for fileid = 0:(length(numFiles)-1)
        fprintf('%d/%d\n', fileid+1, length(numFiles));
        % Get annotation
        jointFile = sprintf([origDir '/joint/im%04d.csv'], fileid);
        [X, Y] = read_joint_info(jointFile);

        % Get foreground mask
        depth_fname = sprintf([origDir '/depth/im%04d.png'], fileid);
        part_fname = sprintf([origDir '/paint/im%04d.png'], fileid);
        if exist(depth_fname, 'file')
            depth = imread(depth_fname);
            fgMask = depth(:,:,1) > 0;
        elseif exist(part_fname, 'file')
            p = imread(part_fname);
            fgMask = ~(p(:,:,1) == 0 & p(:,:,2) == 0 & p(:,:,3) == 0);
        else
            fprintf('No avaliable foreground information for image %04d\n', fileid);
            continue;
        end
        

        for type = {'imgs', 'depth', 'paint'}
            type = type{1};
            imfname = sprintf([origDir '/' type '/im%04d.png'], fileid);
            if ~exist(imfname, 'file') 
                continue; 
            end
            
            im = imread(imfname);
            im = im2double(im);
            
            [crop, U, V] = crop_img(im, fgMask, X, Y);
            % debug
            % imshow(im); hold on; plot(X, Y, '*'); pause;
            % imshow(crop); hold on; plot(U, V, '*'); pause;
            
            % Save cropped image
            crop_imfname = sprintf([cropDir '/' type '/im%04d.png'], fileid);
            imwrite(crop, crop_imfname);

            % Save annotation
            joints(1, :, fileid+1) = U;
            joints(2, :, fileid+1) = V;
        end
    end
    save([cropDir 'joints-PC.mat'], 'joints');
end


